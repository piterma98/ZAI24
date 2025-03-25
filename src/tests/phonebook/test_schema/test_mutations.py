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
        "groups": groups,
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
                    "groups": groups,
                }
            }
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
    assert PhonebookEntry.objects.all().count() == 1
