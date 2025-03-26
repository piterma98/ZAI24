import logging
from dataclasses import dataclass

from django.core.exceptions import ValidationError
from django.db import transaction

from phonebook.exceptions import PhonebookError
from phonebook.models import PhonebookEntry, PhonebookGroup, PhonebookNumber
from users.models import User

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AddPhonebookEntryNumberData:
    number_type: str
    number: str


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
        created_by: User,
    ) -> PhonebookEntry:
        try:
            phonebook_entry = PhonebookEntry.objects.create(
                name=name,
                city=city,
                street=street,
                postal_code=postal_code,
                country=country,
                type=type,
                created_by=created_by,
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
            raise PhonebookError(reason="Error while creating phonebook entry!")
        return phonebook_entry

    @transaction.atomic
    def update(
        self,
        user: User,
        entry_id: int,
        name: str | None = None,
        city: str | None = None,
        street: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
        type: str | None = None,
    ) -> PhonebookEntry:
        try:
            entry = PhonebookEntry.objects.get(id=entry_id)
            if entry.created_by != user:
                logger.error("Failed to update entry")
                raise PhonebookError(reason="You are not owner of this entry")
            fields_to_update: list[str] = []
            if name:
                entry.name = name
                fields_to_update.append("name")
            if city:
                entry.city = city
                fields_to_update.append("city")
            if street:
                entry.street = street
                fields_to_update.append("street")
            if postal_code:
                entry.postal_code = postal_code
                fields_to_update.append("postal_code")
            if country:
                entry.country = country
                fields_to_update.append("country")
            if type:
                entry.type = type
                fields_to_update.append("type")
            entry.full_clean()
            entry.save(update_fields=fields_to_update)
        except (PhonebookEntry.DoesNotExist, ValidationError) as e:
            logger.error(f"Failed to update entry {e}")
            raise PhonebookError(reason="Failed to update entry!") from e
        return entry

    @transaction.atomic
    def delete(
        self,
        user: User,
        entry_id: int,
    ) -> None:
        try:
            entry = PhonebookEntry.objects.get(id=entry_id)
            if entry.created_by != user:
                logger.error("Failed to update entry")
                raise PhonebookError(reason="You are not owner of this entry")
            entry.delete()
        except PhonebookEntry.DoesNotExist as e:
            logger.error(f"Failed to delete entry {e}")
            raise PhonebookError(reason="Entry with given id does not exists!") from e

    @transaction.atomic
    def add_to_group(self, user: User, entry_id: int, group: str) -> PhonebookEntry:
        try:
            entry = PhonebookEntry.objects.get(id=entry_id)
            if entry.created_by != user:
                logger.error("Failed to update entry")
                raise PhonebookError(reason="You are not owner of this entry")
            phonebook_group, _ = PhonebookGroup.objects.get_or_create(name=group)
            entry.groups.add(phonebook_group)
            return entry
        except PhonebookEntry.DoesNotExist as e:
            logger.error(f"Failed to add entry to group {e}")
            raise PhonebookError(reason="Entry with given id does not exists!") from e

    @transaction.atomic
    def remove_from_group(self, user: User, entry_id: int, group: str) -> None:
        try:
            entry = PhonebookEntry.objects.get(id=entry_id)
            if entry.created_by != user:
                logger.error("Failed to update entry")
                raise PhonebookError(reason="You are not owner of this entry")
            phonebook_group = PhonebookGroup.objects.get(name=group)
            entry.groups.remove(phonebook_group)
        except (PhonebookEntry.DoesNotExist, PhonebookGroup.DoesNotExist) as e:
            logger.error(f"Failed to delete entry group {e}")
            raise PhonebookError(reason="Failed to delete entry group!") from e

    @transaction.atomic
    def add_number(self, entry_id: int, user: User, number: str, number_type: str) -> PhonebookEntry:
        try:
            entry = PhonebookEntry.objects.get(id=entry_id)
            if entry.created_by != user:
                logger.error("Failed to update entry")
                raise PhonebookError(reason="You are not owner of this entry")
            phonebook_number = PhonebookNumber.objects.create(
                phonebook_entry=entry,
                type=number_type,
                number=number,
            )
            phonebook_number.full_clean()
            return entry
        except (PhonebookEntry.DoesNotExist, ValidationError) as e:
            logger.error(f"Failed to add entry number {e}")
            raise PhonebookError(reason="Failed to add entry number!") from e

    @transaction.atomic
    def remove_number(self, entry_number_id: int, user: User) -> PhonebookEntry:
        try:
            number = PhonebookNumber.objects.select_related("phonebook_entry__created_by").get(id=entry_number_id)
            if number.phonebook_entry.created_by == user:
                number.delete()
            else:
                logger.error("Failed to remove entry number")
                raise PhonebookError(reason="You are not owner of this entry")
            return number.phonebook_entry
        except PhonebookNumber.DoesNotExist as e:
            logger.error(f"Failed to remove entry number {e}")
            raise PhonebookError(reason="Failed to remove entry number!") from e
