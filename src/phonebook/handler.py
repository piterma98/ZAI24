import logging
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction

from api.exceptions import InputIdTypeMismatchError
from api.graphql_utils import validate_gid
from phonebook.models import PhonebookEntry, PhonebookGroup, PhonebookNumber
from users.models import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddPhonebookEntryNumberData:
    number_type: str
    number: str


class PhonebookError(Exception):
    def __init__(self, reason: str, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason


class PhonebookHandler:
    @transaction.atomic
    def create(
        self,
        name: str,
        city: str,
        street: str,
        postal_code: str,
        country: str,
        type: str,
        groups: list[str],
        numbers: list[AddPhonebookEntryNumberData],
    ) -> PhonebookEntry:
        try:
            phonebook_entry = PhonebookEntry.objects.create(
                name=name, city=city, street=street, postal_code=postal_code, country=country, type=type
            )
            phonebook_entry.full_clean()
            group_list = []
            for group in groups:
                phonebook_group, _ = PhonebookGroup.objects.get_or_create(name=group)
                group_list.append(phonebook_group)
            phonebook_entry.groups.set(group_list)
            for number in numbers:
                PhonebookNumber.objects.create(
                    phonebook_entry=phonebook_entry,
                    type=number.number_type,
                    number=number.number,
                )
        except ValidationError as e:
            logger.warning(f"Error while creating phonebook entry {e}")
            raise PhonebookError(reason=f"Error while creating phonebook entry {e}")
        return phonebook_entry

    @transaction.atomic
    def update(
        self,
        entry_id: str,
        name: str | None = None,
        city: str | None = None,
        street: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
        type: str | None = None,
    ) -> PhonebookEntry:
        try:
            entry = PhonebookEntry.objects.get(id=int(validate_gid(entry_id, "PhonebookEntryNode")))
            fields_to_update: list[str] = []
            if name:
                entry.name = name
                fields_to_update.append("name")
            if city:
                entry.name = city
                fields_to_update.append("city")
            if street:
                entry.name = street
                fields_to_update.append("street")
            if postal_code:
                entry.name = postal_code
                fields_to_update.append("postal_code")
            if country:
                entry.name = country
                fields_to_update.append("country")
            if type:
                entry.name = type
                fields_to_update.append("type")
            entry.full_clean()
            entry.save(update_fields=fields_to_update)
        except (PhonebookEntry.DoesNotExist, InputIdTypeMismatchError, ValidationError) as e:
            logger.error(f"Failed to update entry {e}")
            raise PhonebookError(reason="Failed to update entry!") from e
        return entry

    @transaction.atomic
    def delete(
        self,
        entry_id: str,
    ) -> None:
        try:
            entry = PhonebookEntry.objects.get(id=int(validate_gid(entry_id, "PhonebookEntryNode")))
            entry.delete()
        except (PhonebookEntry.DoesNotExist, InputIdTypeMismatchError) as e:
            logger.error(f"Failed to delete entry {e}")
            raise PhonebookError(reason="Failed to delete entry!") from e

    @transaction.atomic
    def add_to_group(self, entry_id: str, group: str):
        try:
            entry = PhonebookEntry.objects.get(id=int(validate_gid(entry_id, "PhonebookEntryNode")))
            phonebook_group, _ = PhonebookGroup.objects.get_or_create(name=group)
            entry.groups.add(phonebook_group)
        except (PhonebookEntry.DoesNotExist, InputIdTypeMismatchError) as e:
            logger.error(f"Failed to add entry to group {e}")
            raise PhonebookError(reason="Failed to add entry to group!") from e

    @transaction.atomic
    def remove_from_group(self, entry_id: str, group: str):
        try:
            entry = PhonebookEntry.objects.get(id=int(validate_gid(entry_id, "PhonebookEntryNode")))
            phonebook_group = PhonebookGroup.objects.get(name=group)
            entry.groups.remove(phonebook_group)
        except (PhonebookEntry.DoesNotExist, PhonebookGroup.DoesNotExist, InputIdTypeMismatchError) as e:
            logger.error(f"Failed to delete entry group {e}")
            raise PhonebookError(reason="Failed to delete entry group!") from e

    @transaction.atomic
    def add_number(self, entry_id: str, number: str, number_type: str):
        try:
            entry = PhonebookEntry.objects.get(id=int(validate_gid(entry_id, "PhonebookEntryNode")))
            phonebook_number = PhonebookNumber.objects.create(
                phonebook_entry=entry,
                type=number_type,
                number=number,
            )
            phonebook_number.full_clean()
        except (PhonebookEntry.DoesNotExist, InputIdTypeMismatchError, ValidationError) as e:
            logger.error(f"Failed to add entry number {e}")
            raise PhonebookError(reason="Failed to add entry number!") from e

    @transaction.atomic
    def remove_number(self, entry_number_id: str, user: User):
        try:
            number = PhonebookNumber.objects.select_related("phonebook_entry__created_by").get(
                id=int(validate_gid(entry_number_id, "PhonebookNumbersNode"))
            )
            if number.phonebook_entry.created_by == user:
                number.delete()
            else:
                logger.error("Failed to remove entry number")
                raise PhonebookError(reason="You are not owner of this entry")
        except (PhonebookNumber.DoesNotExist, InputIdTypeMismatchError) as e:
            logger.error(f"Failed to remove entry number {e}")
            raise PhonebookError(reason="Failed to add entry number!") from e
