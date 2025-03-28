from django.contrib import admin

from model_utils import BaseModelAdmin
from phonebook.models import PhonebookEntry, PhonebookEntryRating, PhonebookGroup, PhonebookNumber


@admin.register(PhonebookEntry)
class PhonebookEntryAdmin(BaseModelAdmin): ...


@admin.register(PhonebookGroup)
class PhonebookGroupAdmin(BaseModelAdmin): ...


@admin.register(PhonebookNumber)
class PhonebookNumberAdmin(BaseModelAdmin): ...


@admin.register(PhonebookEntryRating)
class PhonebookEntryRatingAdmin(BaseModelAdmin): ...
