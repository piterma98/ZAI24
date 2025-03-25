import logging

import graphene
from graphene import ClientIDMutation

from api.exceptions import InputIdTypeMismatchError
from api.graphql_utils import login_required, validate_gid
from phonebook.handler import AddPhonebookEntryNumberData, PhonebookError, PhonebookHandler
from phonebook.user_schema.queries import NumberTypeEnum, PhonebookEntryNode, TypeEnum

logger = logging.getLogger(__name__)


class AddPhonebookEntrySuccess(graphene.ObjectType):
    phonebook = graphene.Field(PhonebookEntryNode)


class AddPhonebookEntryError(graphene.ObjectType):
    reason = graphene.String()


class AddPhonebookEntryResult(graphene.Union):
    class Meta:
        types = (AddPhonebookEntrySuccess, AddPhonebookEntryError)


class AddPhonebookEntryNumberInputData(graphene.InputObjectType):
    number_type = NumberTypeEnum(required=True)
    number = graphene.String(required=True)


class AddPhonebookEntry(ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        city = graphene.String(required=True)
        street = graphene.String(required=True)
        postal_code = graphene.String(required=True)
        country = graphene.String(required=True)
        type = TypeEnum(required=True)
        groups = graphene.List(graphene.String, required=True)
        numbers = graphene.List(AddPhonebookEntryNumberInputData, required=True)

    result = graphene.Field(AddPhonebookEntryResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        name: str,
        city: str,
        street: str,
        postal_code: str,
        country: str,
        type: str,
        groups: list[str],
        numbers: list[AddPhonebookEntryNumberData],
    ) -> "AddPhonebookEntry":
        try:
            entry = PhonebookHandler().create(
                name=name,
                city=city,
                street=street,
                postal_code=postal_code,
                country=country,
                type=type,
                groups=groups,
                numbers=[
                    AddPhonebookEntryNumberData(
                        number=number.number,
                        number_type=number.number_type,
                    )
                    for number in numbers
                ],
                created_by=info.context.user,
            )
            return cls(result=AddPhonebookEntrySuccess(phonebook=entry))
        except PhonebookError as e:
            return cls(result=AddPhonebookEntryError(reason=e.reason))


class UpdatePhonebookEntrySuccess(graphene.ObjectType):
    phonebook = graphene.Field(PhonebookEntryNode)


class UpdatePhonebookEntryError(graphene.ObjectType):
    reason = graphene.String()


class UpdatePhonebookEntryResult(graphene.Union):
    class Meta:
        types = (UpdatePhonebookEntrySuccess, UpdatePhonebookEntryError)


class UpdatePhonebookEntry(ClientIDMutation):
    class Input:
        entry_id = graphene.ID(required=True)
        name = graphene.String(required=False)
        city = graphene.String(required=False)
        street = graphene.String(required=False)
        postal_code = graphene.String(required=False)
        country = graphene.String(required=False)
        type = TypeEnum(required=False)

    result = graphene.Field(UpdatePhonebookEntryResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        entry_id: str,
        name: str | None = None,
        city: str | None = None,
        street: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
        type: str | None = None,
    ) -> "UpdatePhonebookEntry":
        try:
            entry = PhonebookHandler().update(
                user=info.context.user,
                entry_id=int(validate_gid(entry_id, "PhonebookEntryNode")),
                name=name,
                city=city,
                street=street,
                postal_code=postal_code,
                country=country,
                type=type,
            )
            return cls(result=UpdatePhonebookEntrySuccess(phonebook=entry))
        except InputIdTypeMismatchError:
            return cls(result=UpdatePhonebookEntryError(reason="Invalid phonebook entry id!"))
        except PhonebookError as e:
            return cls(result=UpdatePhonebookEntryError(reason=e.reason))


class DeletePhonebookEntrySuccess(graphene.ObjectType):
    is_deleted = graphene.Boolean()


class DeletePhonebookEntryError(graphene.ObjectType):
    reason = graphene.String()


class DeletePhonebookEntryResult(graphene.Union):
    class Meta:
        types = (DeletePhonebookEntrySuccess, DeletePhonebookEntryError)


class DeletePhonebookEntry(ClientIDMutation):
    class Input:
        photo_id = graphene.ID(required=True)

    result = graphene.Field(DeletePhonebookEntryResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        phonebook_entry_id: str,
    ) -> "DeletePhonebookEntry":
        try:
            PhonebookHandler().delete(
                user=info.context.user, entry_id=int(validate_gid(phonebook_entry_id, "PhonebookEntryNode"))
            )
            return cls(result=DeletePhonebookEntrySuccess(is_deleted=True))
        except InputIdTypeMismatchError:
            return cls(result=DeletePhonebookEntryError(reason="Invalid phonebook entry id!"))
        except PhonebookError as e:
            return cls(result=DeletePhonebookEntryError(reason=e.reason))


class AddPhonebookEntryGroupSuccess(graphene.ObjectType):
    phonebook = graphene.Field(PhonebookEntryNode)


class AddPhonebookEntryGroupError(graphene.ObjectType):
    reason = graphene.String()


class AddPhonebookEntryGroupResult(graphene.Union):
    class Meta:
        types = (AddPhonebookEntryGroupSuccess, AddPhonebookEntryGroupError)


class AddPhonebookEntryGroup(ClientIDMutation):
    class Input:
        phonebook_entry_id = graphene.ID(required=True)
        group = graphene.String(required=True)

    result = graphene.Field(AddPhonebookEntryGroupResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        phonebook_entry_id: str,
        group: str,
    ) -> "AddPhonebookEntry":
        try:
            entry = PhonebookHandler().add_to_group(
                user=info.context.user,
                entry_id=int(validate_gid(phonebook_entry_id, "PhonebookEntryNode")),
                group=group,
            )
            return cls(result=AddPhonebookEntryGroupSuccess(phonebook=entry))
        except InputIdTypeMismatchError:
            return cls(result=AddPhonebookEntryGroupError(reason="Invalid phonebook entry id!"))
        except PhonebookError as e:
            return cls(result=AddPhonebookEntryGroupError(reason=e.reason))


class RemovePhonebookEntryGroupSuccess(graphene.ObjectType):
    is_deleted = graphene.Boolean()


class RemovePhonebookEntryGroupError(graphene.ObjectType):
    reason = graphene.String()


class RemovePhonebookEntryGroupResult(graphene.Union):
    class Meta:
        types = (RemovePhonebookEntryGroupSuccess, RemovePhonebookEntryGroupError)


class RemovePhonebookEntryGroup(ClientIDMutation):
    class Input:
        phonebook_entry_id = graphene.ID(required=True)
        group = graphene.String(required=True)

    result = graphene.Field(RemovePhonebookEntryGroupResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        phonebook_entry_id: str,
        group: str,
    ) -> "RemovePhonebookEntryGroup":
        try:
            PhonebookHandler().remove_from_group(
                user=info.context.user,
                entry_id=int(validate_gid(phonebook_entry_id, "PhonebookEntryNode")),
                group=group,
            )
            return cls(result=RemovePhonebookEntryGroupSuccess(is_deleted=True))
        except InputIdTypeMismatchError:
            return cls(result=RemovePhonebookEntryGroupError(reason="Invalid phonebook entry id!"))
        except PhonebookError as e:
            return cls(result=RemovePhonebookEntryGroupError(reason=e.reason))


class AddPhonebookEntryNumberSuccess(graphene.ObjectType):
    phonebook = graphene.Field(PhonebookEntryNode)


class AddPhonebookEntryNumberError(graphene.ObjectType):
    reason = graphene.String()


class AddPhonebookEntryNumberResult(graphene.Union):
    class Meta:
        types = (AddPhonebookEntryGroupSuccess, AddPhonebookEntryGroupError)


class AddPhonebookEntryNumber(ClientIDMutation):
    class Input:
        phonebook_entry_id = graphene.ID(required=True)
        number_type = NumberTypeEnum(required=True)
        number = graphene.String(required=True)

    result = graphene.Field(AddPhonebookEntryNumberSuccess)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        phonebook_entry_id: str,
        number: str,
        number_type: str,
    ) -> "AddPhonebookEntryNumber":
        try:
            entry = PhonebookHandler().add_number(
                user=info.context.user,
                entry_id=int(validate_gid(phonebook_entry_id, "PhonebookEntryNode")),
                number=number,
                number_type=number_type,
            )
            return cls(result=AddPhonebookEntryGroupSuccess(phonebook=entry))
        except InputIdTypeMismatchError:
            return cls(result=AddPhonebookEntryGroupError(reason="Invalid phonebook entry id!"))
        except PhonebookError as e:
            return cls(result=AddPhonebookEntryGroupError(reason=e.reason))


class RemovePhonebookEntryNumberSuccess(graphene.ObjectType):
    is_deleted = graphene.Boolean()


class RemovePhonebookEntryNumberError(graphene.ObjectType):
    reason = graphene.String()


class RemovePhonebookEntryNumberResult(graphene.Union):
    class Meta:
        types = (RemovePhonebookEntryNumberSuccess, RemovePhonebookEntryNumberError)


class RemovePhonebookEntryNumberGroup(ClientIDMutation):
    class Input:
        phonebook_entry_id = graphene.ID(required=True)
        group = graphene.String(required=True)

    result = graphene.Field(RemovePhonebookEntryNumberResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        phonebook_entry_id: str,
    ) -> "RemovePhonebookEntryGroup":
        try:
            PhonebookHandler().remove_number(
                user=info.context.user,
                entry_number_id=int(validate_gid(phonebook_entry_id, "PhonebookNumberNode")),
            )
            return cls(result=RemovePhonebookEntryNumberSuccess(is_deleted=True))
        except InputIdTypeMismatchError:
            return cls(result=RemovePhonebookEntryNumberError(reason="Invalid phonebook number id!"))
        except PhonebookError as e:
            return cls(result=RemovePhonebookEntryNumberError(reason=e.reason))


class Mutation(graphene.ObjectType):
    add_phonebook_entry = AddPhonebookEntry.Field()
    update_phonebook_entry = UpdatePhonebookEntry.Field()
    delete_phonebook_entry = DeletePhonebookEntry.Field()
    add_phonebook_entry_group = AddPhonebookEntryGroup.Field()
    remove_phonebook_entry_group = RemovePhonebookEntryGroup.Field()
    add_phonebook_entry_number = AddPhonebookEntryNumber.Field()
