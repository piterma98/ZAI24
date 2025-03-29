from decimal import Decimal

import graphene
from django.db.models import QuerySet
from django.db.models.aggregates import Avg, Count
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


class PhonebookNumberNode(DjangoObjectType):
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
    numbers = graphene.List(PhonebookNumberNode)
    groups = graphene.List(graphene.String)
    rating = graphene.Decimal()
    rating_count = graphene.Int()

    class Meta:
        model = PhonebookEntry
        fields = ("name", "city", "street", "postal_code", "country")
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

    def resolve_numbers(self, info: graphene.ResolveInfo) -> QuerySet["PhonebookNumber"]:
        return self.phonebook_number.all()

    def resolve_groups(self, info: graphene.ResolveInfo) -> list[str]:
        return self.groups.all().values_list("name", flat=True)

    def resolve_rating(self, info: graphene.ResolveInfo) -> Decimal:
        return round(Decimal(self.phonebook_rating.aggregate(Avg("rate", default=0))["rate__avg"]), 2)

    def resolve_rating_count(self, info: graphene.ResolveInfo) -> int:
        return self.rating__count


class Query(graphene.ObjectType):
    phonebook_entry = DjangoFilterConnectionField(PhonebookEntryNode)
    phonebook_entry_count = graphene.Int()

    def resolve_phonebook_entry(self, info: graphene.ResolveInfo, **kwargs) -> QuerySet[PhonebookEntry]:
        return (
            PhonebookEntry.objects.annotate(rating__count=Count("phonebook_rating"))
            .prefetch_related("groups", "phonebook_number")
            .all()
        )

    def resolve_phonebook_entry_count(self, info: graphene.ResolveInfo, **kwargs) -> int:
        return PhonebookEntry.objects.all().count()
