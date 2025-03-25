import pytest
from graphql_relay import to_global_id


@pytest.mark.django_db
def test_user_query_me(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user(
        email="janusz@cebula.com",
        firstname="Janusz",
        lastname="Tracz",
    )
    user_schema_client.user = user
    query = """
          query Me {
            me {
              id
              email
              lastName
              firstName
            }
          }
        """

    result = user_schema_client.execute(query)
    expected = {
        "me": {
            "id": to_global_id("Me", user.id),
            "email": "janusz@cebula.com",
            "lastName": "Tracz",
            "firstName": "Janusz",
        }
    }

    assert "errors" not in result
    assert result["data"] == expected


def test_user_query_unauthenticated(user_schema_anonymous_client) -> None:
    query = """
          query Me {
            me {
              id
              email
              lastName
              firstName
            }
          }
        """

    result = user_schema_anonymous_client.execute(query)

    assert result["errors"][0]["message"] == "AuthenticationError"
