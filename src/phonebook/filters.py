from django_filters import CharFilter, FilterSet, OrderingFilter

from model_utils import SearchableFilterSetMixin
from phonebook.models import PhonebookEntry


class PhonebookFilterSet(SearchableFilterSetMixin, FilterSet):
    class Meta:
        model = PhonebookEntry
        fields = {"type": ["exact"], "city": ["exact"]}

    search_fields: list[str] = ["name", "city", "groups__name"]
    search = CharFilter(method="search_filter")
    order_by = OrderingFilter(
        fields={
            "created_at": "created_at",
        }
    )
