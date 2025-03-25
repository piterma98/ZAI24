import graphene
from django.db.models import QuerySet
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from phonebook.filters import PhonebookFilterSet
from phonebook.models import (
    PhonebookEntry,
    PhonebookEntryTypeEnum,
    PhonebookGroup,
    PhonebookNumber,
    PhonebookNumberTypeEnum,
)

TypeEnum = graphene.Enum.from_enum(PhonebookEntryTypeEnum, name="PhonebookEntryTypeEnum")
NumberTypeEnum = graphene.Enum.from_enum(PhonebookNumberTypeEnum, name="PhonebookNumberTypeEnum")


class PhonebookNumbersNode(DjangoObjectType):
    type = NumberTypeEnum()

    class Meta:
        model = PhonebookNumber
        fields = ("number",)
        interfaces = (graphene.relay.Node,)


class PhonebookGroupNode(DjangoObjectType):
    class Meta:
        model = PhonebookGroup
        fields = ("name",)


class PhonebookEntryNode(DjangoObjectType):
    type = TypeEnum()
    numbers = graphene.List(PhonebookNumbersNode)
    groups = graphene.List(graphene.String)

    class Meta:
        model = PhonebookEntry
        fields = ("name", "city", "street", "postal_code")
        interfaces = (graphene.relay.Node,)
        filterset_class = PhonebookFilterSet

    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, id: int) -> PhonebookEntry | None:
        queryset = cls.get_queryset(cls._meta.model.objects, info)
        try:
            obj = queryset.get(pk=id)
            if obj.created_by == info.context.user:
                return obj
            return None
        except cls._meta.model.DoesNotExist:
            return None

    def resolve_numbers(self, info: graphene.ResolveInfo) -> list[str]:
        return self.phonebook_number.all()

    def resolve_groups(self, info: graphene.ResolveInfo) -> list[str]:
        return self.groups.all().values_list("name", flat=True)


class Query(graphene.ObjectType):
    phonebook_entry = DjangoFilterConnectionField(PhonebookEntryNode)
    phonebook_entry_count = graphene.Int()

    def resolve_phonebook_entry(self, info: graphene.ResolveInfo, **kwargs) -> QuerySet[PhonebookEntry]:
        # check number of queries
        return PhonebookEntry.objects.prefetch_related("groups", "phonebook_number").all()

    def resolve_phonebook_entry_count(self, info: graphene.ResolveInfo, **kwargs) -> int:
        # check number of queries
        return PhonebookEntry.objects.all().count()
