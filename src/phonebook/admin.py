from django.contrib import admin

from model_utils import BaseModelAdmin
from phonebook.models import PhonebookEntry, PhonebookGroup, PhonebookNumber


@admin.register(PhonebookEntry)
class PhonebookEntryAdmin(BaseModelAdmin): ...


@admin.register(PhonebookGroup)
class PhonebookGroupAdmin(BaseModelAdmin): ...


@admin.register(PhonebookNumber)
class PhonebookNumberAdmin(BaseModelAdmin): ...
