import itertools
from typing import TypeVar

from django.contrib import admin
from django.db import models
from django.db.models import Q, QuerySet, Value
from django.http import HttpRequest
from graphql_relay import to_global_id

M = TypeVar("M", bound=models.Model)


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request: HttpRequest, obj: models.Model | None = None) -> list[str] | tuple[str, ...]:
        if obj:
            return tuple(itertools.chain(self.readonly_fields, ("created", "modified")))
        return self.readonly_fields


class GrapheneModelMixin:
    id: int

    @property
    def gid(self) -> str:
        return to_global_id(f"{self.__class__.__name__}Node", self.id)


class SearchableFilterSetMixin:
    """
    Mixin for FilterSet search implementation.
    Add search = CharFilter(method="search_filter")
    field to FilterSet class to make it work.
    """

    search_fields: list[str]

    def search_filter(self, queryset: QuerySet[M], name: str, value: str) -> QuerySet[M]:
        if not value:
            return queryset
        q = Q()
        for search_field in self.search_fields:
            q.add(Q(**{f"{search_field}__icontains": Value(value)}), Q.OR)
        return queryset.filter(q).distinct()
