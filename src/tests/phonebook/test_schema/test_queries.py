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
                slug
                name
                city
                postalCode
                street
                country
                rating
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
                        "slug": entry.slug,
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "rating": "0.00",
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
                slug
                name
                city
                postalCode
                street
                country
                rating
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
                        "slug": entry.slug,
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "rating": "0.00",
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
              slug
              name
              city
              postalCode
              street
              country
              rating
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
            "slug": entry.slug,
            "city": entry.city,
            "postalCode": entry.postal_code,
            "street": entry.street,
            "country": entry.country,
            "rating": "0.00",
            "numbers": [
                {"number": "500500500", "type": "mobile"},
            ],
            "groups": list(entry.groups.all().values_list("name", flat=True)),
        }
    }

    assert "errors" not in result
    assert result["data"] == expected


@pytest.mark.django_db
def test_phonebook_entry_user_query(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    user_2 = data_fixture.create_user()
    entry_1 = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry_1, "500500500", "mobile")
    entry_2 = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False)
    data_fixture.add_phonebook_entry_number(entry_2, "226465020", "landline")
    _ = data_fixture.create_phonebook_entry(created_by=user_2)
    user_schema_client.user = user
    query = """
        query Me {
          me {
            myPhonebookEntries {
              edges {
                node {
                  slug
                  name
                  city
                  postalCode
                  street
                  country
                  rating
                  numbers {
                    number
                    type
                  }
                  groups
                }
              }
            }
          }
        }
        """
    result = user_schema_client.execute(query)
    expected = {
        "me": {
            "myPhonebookEntries": {
                "edges": [
                    {
                        "node": {
                            "slug": entry_1.slug,
                            "name": entry_1.name,
                            "city": entry_1.city,
                            "postalCode": entry_1.postal_code,
                            "street": entry_1.street,
                            "country": entry_1.country,
                            "rating": "0.00",
                            "numbers": [
                                {"number": "500500500", "type": "mobile"},
                            ],
                            "groups": list(entry_1.groups.all().values_list("name", flat=True)),
                        }
                    },
                    {
                        "node": {
                            "slug": entry_2.slug,
                            "name": entry_2.name,
                            "city": entry_2.city,
                            "postalCode": entry_2.postal_code,
                            "street": entry_2.street,
                            "country": entry_2.country,
                            "rating": "0.00",
                            "numbers": [
                                {"number": "226465020", "type": "landline"},
                            ],
                            "groups": list(entry_2.groups.all().values_list("name", flat=True)),
                        }
                    },
                ]
            }
        }
    }

    assert "errors" not in result
    assert len(result["data"]["me"]["myPhonebookEntries"]["edges"]) == 2
    assert result["data"] == expected


@pytest.mark.django_db
def test_phonebook_entry_rating_query(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False, create_groups=False)
    data_fixture.add_phonebook_entry_rating(entry, 5, user)
    data_fixture.add_phonebook_entry_rating(entry, 0, user)
    data_fixture.add_phonebook_entry_rating(entry, 3, user)

    user_schema_client.user = user
    query = """
           query Phonebook{
             phonebookEntryCount
             phonebookEntry{
               edges
               {
                 node{
                   id
                   slug
                   name
                   city
                   postalCode
                   street
                   country
                   rating
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
                        "slug": entry.slug,
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "rating": "2.67",
                    }
                }
            ]
        },
    }

    assert "errors" not in result
    assert result["data"] == expected
    assert entry.phonebook_rating.all().count() == 3


@pytest.mark.django_db
def test_phonebook_entry_rating_count_query(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user()
    entry = data_fixture.create_phonebook_entry(created_by=user, create_numbers=False, create_groups=False)
    data_fixture.add_phonebook_entry_rating(entry, 5, user)
    data_fixture.add_phonebook_entry_rating(entry, 0, user)
    data_fixture.add_phonebook_entry_rating(entry, 3, user)

    user_schema_client.user = user
    query = """
            query Phonebook {
              phonebookEntryCount
              phonebookEntry {
                edges {
                  node {
                    id
                    slug
                    name
                    city
                    postalCode
                    street
                    country
                    rating
                    ratingCount
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
                        "slug": entry.slug,
                        "name": entry.name,
                        "city": entry.city,
                        "postalCode": entry.postal_code,
                        "street": entry.street,
                        "country": entry.country,
                        "rating": "2.67",
                        "ratingCount": 3,
                    }
                }
            ]
        },
    }

    assert "errors" not in result
    assert result["data"] == expected
    assert entry.phonebook_rating.all().count() == 3
