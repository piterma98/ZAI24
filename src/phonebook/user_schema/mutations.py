import logging

import graphene
from graphene import ClientIDMutation

from api.graphql_utils import login_required
from phonebook.handler import PhonebookHandler
from phonebook.user_schema.queries import PhonebookEntryNode

logger = logging.getLogger(__name__)


class AddPhonebookEntrySuccess(graphene.ObjectType):
    surface = graphene.Field(PhonebookEntryNode)


class AddPhonebookEntryError(graphene.ObjectType):
    reason = graphene.String()


class AddPhonebookEntryResult(graphene.Union):
    class Meta:
        types = (AddPhonebookEntrySuccess, AddPhonebookEntryError)


class AddPhonebookEntry(ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        category = graphene.ID(required=True)
        description = graphene.String(required=True)
        numbers = graphene.String(required=True)
        groups = graphene.List(graphene.String, required=True)

    result = graphene.Field(AddPhonebookEntryResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        name: str,
        description: str,
        technical_specification: str,
        category: str,
        surface_formats: list[str],
    ) -> "AddPhonebookEntry":
        entry = PhonebookHandler().create()
        return entry
        # try:
        #     entry = PhonebookHandler().create()
        #     return cls(result=AddPhonebookEntrySuccess(surface=entry))
        # except SurfaceException as e:
        #     return cls(result=AddPhonebookEntryError(reason=e.reason))


class Mutation(graphene.ObjectType):
    add_phonebook_entry = AddPhonebookEntry.Field()
