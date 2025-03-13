import itertools

from django.contrib import admin
from django.db import models


class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BaseModelAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None) -> list[str] | tuple[str, ...]:
        if obj:
            return tuple(
                itertools.chain(self.readonly_fields, ("created_at", "updated_at"))
            )
        return self.readonly_fields
