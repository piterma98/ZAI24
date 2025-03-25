import pytest

from phonebook.handler import AddPhonebookEntryNumberData, PhonebookError, PhonebookHandler
from phonebook.models import PhonebookEntry, PhonebookNumber


@pytest.mark.django_db
def test_phonebook_handler_create_entry(data_fixture) -> None:
    user = data_fixture.create_user()
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
        created_by=user,
    )

    assert entry.name == name
    assert entry.city == city
    assert entry.street == street
    assert entry.postal_code == postal_code
    assert entry.country == country
    assert entry.type == type
    assert entry.groups.all().count() == 2
    assert entry.created_by == user
    assert entry.phonebook_number.all().count() == 1
    assert PhonebookEntry.objects.all().count() == 1


@pytest.mark.django_db
def test_phonebook_handler_update_entry(data_fixture) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user)
    name = "Test entry"
    city = "Warsaw"
    street = "Złota 44"
    postal_code = "01-001"
    country = "Poland"
    type = "enterprise"

    PhonebookHandler().update(
        entry_id=entry.id,
        user=user,
        name=name,
        city=city,
        street=street,
        postal_code=postal_code,
        country=country,
        type=type,
    )

    entry.refresh_from_db()
    assert entry.name == name
    assert entry.city == city
    assert entry.street == street
    assert entry.postal_code == postal_code
    assert entry.country == country
    assert entry.type == type


@pytest.mark.django_db
def test_phonebook_handler_update_entry_does_not_exists(data_fixture) -> None:
    user = data_fixture.create_user()
    with pytest.raises(PhonebookError) as e:
        PhonebookHandler().update(
            entry_id=9999,
            user=user,
        )

    assert e.value.reason == "Failed to update entry!"


@pytest.mark.django_db
def test_phonebook_handler_update_entry_does_invalid_user(data_fixture) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user)
    user_2 = data_fixture.create_user()
    with pytest.raises(PhonebookError) as e:
        PhonebookHandler().update(
            entry_id=entry.id,
            user=user_2,
        )

    assert e.value.reason == "You are not owner of this entry"


@pytest.mark.django_db
def test_phonebook_handler_delete_entry(data_fixture) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user)

    PhonebookHandler().delete(
        entry_id=entry.id,
        user=user,
    )

    assert not PhonebookEntry.objects.filter(id=entry.id).exists()
    assert not PhonebookNumber.objects.filter(phonebook_entry__id=entry.id).exists()


@pytest.mark.django_db
def test_phonebook_handler_delete_entry_does_not_exists(data_fixture) -> None:
    user = data_fixture.create_user()
    with pytest.raises(PhonebookError) as e:
        PhonebookHandler().delete(
            entry_id=9999,
            user=user,
        )

    assert e.value.reason == "Entry with given id does not exists!"


@pytest.mark.django_db
def test_phonebook_handler_delete_entry_invalid_user(data_fixture) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user)
    user_2 = data_fixture.create_user()
    with pytest.raises(PhonebookError) as e:
        PhonebookHandler().delete(
            entry_id=entry.id,
            user=user_2,
        )

    assert e.value.reason == "You are not owner of this entry"
