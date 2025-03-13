import itertools

from django.contrib import admin
from django.db import models
from graphql_relay import to_global_id


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None) -> list[str] | tuple[str, ...]:
        if obj:
            return tuple(itertools.chain(self.readonly_fields, ("created_at", "updated_at")))
        return self.readonly_fields


class GrapheneModelMixin:
    id: int

    @property
    def gid(self) -> str:
        return to_global_id(self.__class__.__name__, self.id)
