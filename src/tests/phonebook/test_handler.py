import pytest

from phonebook.handler import AddPhonebookEntryNumberData, PhonebookHandler
from phonebook.models import PhonebookEntry


@pytest.mark.django_db
def test_phonebook_handler_create_entry() -> None:
    name = "Test entry"
    city = "Warsaw"
    street = "Złota 44"
    postal_code = "01-001"
    country = "Poland"
    type = "enterprise"
    groups = ["Company", "Red"]
    numbers = [AddPhonebookEntryNumberData(number="500500500", number_type="mobile")]

    entry = PhonebookHandler().create(
        name=name,
        city=city,
        street=street,
        postal_code=postal_code,
        country=country,
        type=type,
        groups=groups,
        numbers=numbers,
    )

    assert entry.name == name
    assert entry.city == city
    assert entry.street == street
    assert entry.postal_code == postal_code
    assert entry.country == country
    assert entry.type == type
    assert entry.groups.all().count() == 2
    assert entry.phonebook_number.all().count() == 1
    assert PhonebookEntry.objects.all().count() == 1


@pytest.mark.django_db
def test_phonebook_handler_delete_entry() -> None: ...
