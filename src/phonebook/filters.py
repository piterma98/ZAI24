from django_filters import FilterSet

from model_utils import SearchableFilterSetMixin
from phonebook.models import PhonebookEntry


class PhonebookFilterSet(FilterSet, SearchableFilterSetMixin):
    class Meta:
        model = PhonebookEntry
        fields = {"type": ["exact"], "city": ["exact"]}

    search_fields: list[str] = ["name"]
