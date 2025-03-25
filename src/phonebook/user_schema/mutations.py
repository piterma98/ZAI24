import logging

import graphene
from graphene import ClientIDMutation

from api.graphql_utils import login_required
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


class AddPhonebookEntryNumberInput(graphene.InputObjectType):
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
        numbers = graphene.List(AddPhonebookEntryNumberInput, required=True)

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
            )
            return cls(result=AddPhonebookEntrySuccess(phonebook=entry))
        except PhonebookError as e:
            return cls(result=AddPhonebookEntryError(reason=e.reason))


class Mutation(graphene.ObjectType):
    add_phonebook_entry = AddPhonebookEntry.Field()
