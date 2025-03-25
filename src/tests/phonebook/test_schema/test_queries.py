import pytest
from graphql_relay import to_global_id


@pytest.mark.django_db
def test_phonebook_entry_query(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")

    user_schema_client.user = user
    query = """
        query Phonebook{
          phonebookEntryCount
          phonebookEntry{
            edges
            {
              node{
                id
                name
                city
                postalCode
                street
                country
                numbers{
                  number
                  type
                }
                groups
              }
            }
          }
        }
        """

    result = user_schema_client.execute(query)
    expected = {
        "phonebookEntryCount": 1,
        "phonebookEntry": {
            "edges": [
                {
                    "node": {
                        "id": to_global_id("PhonebookEntryNode", entry.id),
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "numbers": [
                            {"number": "500500500", "type": "mobile"},
                        ],
                        "groups": list(entry.groups.all().values_list("name", flat=True)),
                    }
                }
            ]
        },
    }

    assert "errors" not in result
    assert result["data"] == expected


@pytest.mark.django_db
def test_phonebook_entry_query_search(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    name = "Very interesting name"
    city = "Warsaw"
    street = "Złota 44"
    postal_code = "01-001"
    country = "Poland"
    type = "enterprise"
    entry = data_fixture.create_phonebook_entry(
        name=name,
        city=city,
        street=street,
        postal_code=postal_code,
        country=country,
        type=type,
        created_by=user,
        create_numbers=False,
    )
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")
    _ = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    _ = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)

    user_schema_client.user = user
    query = """
        query Phonebook($search: String){
          phonebookEntryCount
          phonebookEntry(search: $search){
            edges
            {
              node{
                id
                name
                city
                postalCode
                street
                country
                numbers{
                  number
                  type
                }
                groups
              }
            }
          }
        }
        """
    variables = {"search": entry.name}
    result = user_schema_client.execute(query, variables)
    expected = {
        "phonebookEntryCount": 3,
        "phonebookEntry": {
            "edges": [
                {
                    "node": {
                        "id": to_global_id("PhonebookEntryNode", entry.id),
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "numbers": [
                            {"number": "500500500", "type": "mobile"},
                        ],
                        "groups": list(entry.groups.all().values_list("name", flat=True)),
                    }
                }
            ]
        },
    }

    assert "errors" not in result
    assert len(result["data"]["phonebookEntry"]["edges"]) == 1
    assert result["data"] == expected


@pytest.mark.django_db
def test_phonebook_entry_query_node(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry, "500500500", "mobile")

    user_schema_client.user = user
    query = """
        query PhonebookEntryNode($id: ID!) {
          node(id: $id) {
            ... on PhonebookEntryNode {
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
        }
        """

    result = user_schema_client.execute(query, {"id": entry.gid})
    expected = {
        "node": {
            "id": to_global_id("PhonebookEntryNode", entry.id),
            "name": entry.name,
            "city": entry.city,
            "postalCode": entry.postal_code,
            "street": entry.street,
            "country": entry.country,
            "numbers": [
                {"number": "500500500", "type": "mobile"},
            ],
            "groups": list(entry.groups.all().values_list("name", flat=True)),
        }
    }

    assert "errors" not in result
    assert result["data"] == expected
