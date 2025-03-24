from django.contrib import admin

from model_utils import BaseModelAdmin
from phonebook.models import PhonebookEntry


@admin.register(PhonebookEntry)
class PhonebookEntryAdmin(BaseModelAdmin): ...
