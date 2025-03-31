import pytest

from phonebook.models import PhonebookEntry


@pytest.mark.django_db
def test_phonebook_entry_add_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    user_schema_client.user = user
    name = "Test entry"
    city = "Warsaw"
    street = "Złota 44"
    postal_code = "01-001"
    country = "Poland"
    type = "enterprise"
    groups = ["Company", "Red"]
    numbers = [{"number": "500500500", "numberType": "mobile"}]
    query = """
        mutation AddPhonebookEntry(
            $name: String!, $city: String!, $street: String!, $postal_code: String!, $country: String!,
            $type: PhonebookEntryTypeEnum!, $groups: [String]!, $numbers: [AddPhonebookEntryNumberInputData]!
            ) {
          addPhonebookEntry(
            input: {
            name: $name, city: $city, street: $street, postalCode: $postal_code,
            country: $country, type: $type, groups: $groups, numbers: $numbers}
          ) {
            result {
              ... on AddPhonebookEntrySuccess {
                phonebook {
                  name
                  city
                  postalCode
                  street
                  country
                  numbers {
                    number
                    type
                  }
                  groups
                }
              }
              ... on AddPhonebookEntryError {
                reason
              }
            }
          }
        }
        """

    variables = {
        "name": name,
        "city": city,
        "street": street,
        "postal_code": postal_code,
        "country": country,
        "type": type,
        "groups": [group.lower() for group in groups],
        "numbers": numbers,
    }
    result = user_schema_client.execute(query, variables)
    expected = {
        "addPhonebookEntry": {
            "result": {
                "phonebook": {
                    "name": name,
                    "city": city,
                    "postalCode": postal_code,
                    "street": street,
                    "country": country,
                    "numbers": [
                        {"number": "500500500", "type": "mobile"},
                    ],
                    "groups": [group.lower() for group in groups],
                }
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    assert PhonebookEntry.objects.all().count() == 1


@pytest.mark.django_db
def test_phonebook_entry_update_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")
    user_schema_client.user = user
    name = "Test entry"
    city = "Warsaw"
    street = "Złota 44"
    postal_code = "01-001"
    country = "Poland"
    type = "enterprise"
    query = """
        mutation UpdatePhonebookEntry(
            $id: ID!, $name: String!, $city: String!, $street: String!, $postal_code: String!,
            $country: String!, $type: PhonebookEntryTypeEnum!
            ) {
          updatePhonebookEntry(
            input: { entryId: $id
            name: $name, city: $city, street: $street, postalCode: $postal_code,
            country: $country, type: $type}
          ) {
            result {
              ... on UpdatePhonebookEntrySuccess {
                phonebook {
                  name
                  city
                  postalCode
                  street
                  country
                  numbers {
                    number
                    type
                  }
                  groups
                }
              }
              ... on UpdatePhonebookEntryError {
                reason
              }
            }
          }
        }
        """

    variables = {
        "id": entry.gid,
        "name": name,
        "city": city,
        "street": street,
        "postal_code": postal_code,
        "country": country,
        "type": type,
    }
    result = user_schema_client.execute(query, variables)
    expected = {
        "updatePhonebookEntry": {
            "result": {
                "phonebook": {
                    "name": name,
                    "city": city,
                    "postalCode": postal_code,
                    "street": street,
                    "country": country,
                    "numbers": [
                        {"number": "500500500", "type": "mobile"},
                    ],
                    "groups": list(entry.groups.all().values_list("name", flat=True)),
                }
            }
        }
    }

    entry.refresh_from_db()
    assert "errors" not in result
    assert result["data"] == expected
    assert entry.name == name
    assert entry.city == city
    assert entry.street == street
    assert entry.postal_code == postal_code
    assert entry.country == country
    assert entry.type == type


@pytest.mark.django_db
def test_phonebook_entry_delete_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")
    user_schema_client.user = user
    query = """
        mutation DeletePhonebookEntry($id: ID!) {
          deletePhonebookEntry(input: {entryId: $id}) {
            result {
              ... on DeletePhonebookEntrySuccess {
                isDeleted
              }
              ... on DeletePhonebookEntryError {
                reason
              }
            }
          }
        }
        """

    variables = {
        "id": entry.gid,
    }
    result = user_schema_client.execute(query, variables)
    expected = {
        "deletePhonebookEntry": {
            "result": {
                "isDeleted": True,
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    assert not PhonebookEntry.objects.filter(id=entry.id).exists()


@pytest.mark.django_db
def test_phonebook_entry_add_group_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False, create_groups=False)
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")
    user_schema_client.user = user
    query = """
        mutation AddPhonebookEntryGroup($id: ID!, $group: String!) {
          addPhonebookEntryGroup(input: {entryId: $id, group: $group}) {
            result {
              ... on AddPhonebookEntryGroupSuccess {
                phonebook {
                  id
                  name
                  city
                  postalCode
                  street
                  country
                  numbers {
                    number
                    type
                  }
                  groups
                }
              }
              ... on AddPhonebookEntryGroupError {
                reason
              }
            }
          }
        }
        """

    variables = {"id": entry.gid, "group": "water"}
    result = user_schema_client.execute(query, variables)
    expected = {
        "addPhonebookEntryGroup": {
            "result": {
                "phonebook": {
                    "id": entry.gid,
                    "name": entry.name,
                    "city": entry.city,
                    "postalCode": entry.postal_code,
                    "street": entry.street,
                    "country": entry.country,
                    "numbers": [
                        {"number": "500500500", "type": "mobile"},
                    ],
                    "groups": ["water"],
                }
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    groups = entry.groups.all()
    assert groups.count() == 1


@pytest.mark.django_db
def test_phonebook_entry_remove_group_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_groups=False)
    data_fixture.add_phonebook_group(entry, "red")
    user_schema_client.user = user
    query = """
        mutation RemovePhonebookEntryGroup($id: ID!, $group: String!) {
          removePhonebookEntryGroup(input: {entryId: $id, group: $group}) {
            result {
              ... on RemovePhonebookEntryGroupSuccess {
                isDeleted
              }
              ... on RemovePhonebookEntryGroupError {
                reason
              }
            }
          }
        }
        """

    variables = {"id": entry.gid, "group": "red"}
    result = user_schema_client.execute(query, variables)
    expected = {
        "removePhonebookEntryGroup": {
            "result": {
                "isDeleted": True,
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    groups = entry.groups.all()
    assert not groups.filter(name="red").exists()
    assert groups.count() == 0
    assert list(groups.values_list("name", flat=True)) == []


@pytest.mark.django_db
def test_phonebook_entry_add_number_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    user_schema_client.user = user
    query = """
        mutation AddPhonebookEntryNumber($id: ID!, $number_type: PhonebookNumberTypeEnum!, $number: String!) {
          addPhonebookEntryNumber(input: {entryId: $id, numberType: $number_type, number: $number}) {
            result {
              ... on AddPhonebookEntryGroupSuccess {
                phonebook {
                  id
                  name
                  city
                  postalCode
                  street
                  country
                  numbers {
                    number
                    type
                  }
                  groups
                }
              }
              ... on AddPhonebookEntryGroupError {
                reason
              }
            }
          }
        }
        """

    variables = {"id": entry.gid, "number_type": "landline", "number": "225032231"}
    result = user_schema_client.execute(query, variables)
    expected = {
        "addPhonebookEntryNumber": {
            "result": {
                "phonebook": {
                    "id": entry.gid,
                    "name": entry.name,
                    "city": entry.city,
                    "postalCode": entry.postal_code,
                    "street": entry.street,
                    "country": entry.country,
                    "numbers": [
                        {"number": "225032231", "type": "landline"},
                    ],
                    "groups": list(entry.groups.all().values_list("name", flat=True)),
                }
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    numbers = entry.phonebook_number.all()
    assert numbers.count() == 1


@pytest.mark.django_db
def test_phonebook_entry_remove_number_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False, create_groups=False)
    number = data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")
    user_schema_client.user = user
    query = """
        mutation RemovePhonebookEntryNumber($id: ID!) {
          removePhonebookEntryNumber(input: {phonebookNumberId: $id,}) {
            result {
              ... on RemovePhonebookEntryNumberSuccess {
                isDeleted
              }
              ... on RemovePhonebookEntryNumberError {
                reason
              }
            }
          }
        }
        """

    variables = {
        "id": number.gid,
    }
    result = user_schema_client.execute(query, variables)
    expected = {
        "removePhonebookEntryNumber": {
            "result": {
                "isDeleted": True,
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    numbers = entry.phonebook_number.all()
    assert numbers.count() == 0


@pytest.mark.django_db
def test_phonebook_entry_add_rating_mutation(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    user_schema_client.user = user
    query = """
        mutation AddPhonebookEntryRate($id: ID!, $rate: Int!) {
          addPhonebookEntryRate(input: {entryId: $id, rate: $rate}) {
            result {
              ... on AddPhonebookEntryRatingSuccess {
                phonebook {
                  id
                  name
                  city
                  postalCode
                  street
                  country
                  rating
                }
              }
              ... on AddPhonebookEntryRatingError {
                reason
              }
            }
          }
        }
        """

    variables = {"id": entry.gid, "rate": 1}
    result = user_schema_client.execute(query, variables)
    expected = {
        "addPhonebookEntryRate": {
            "result": {
                "phonebook": {
                    "id": entry.gid,
                    "name": entry.name,
                    "city": entry.city,
                    "postalCode": entry.postal_code,
                    "street": entry.street,
                    "country": entry.country,
                    "rating": "1.00",
                }
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    ratings = entry.phonebook_rating.all()
    assert ratings.count() == 1
