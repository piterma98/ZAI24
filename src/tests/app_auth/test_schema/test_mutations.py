from unittest.mock import ANY

import pytest
from graphql_jwt.settings import jwt_settings


@pytest.mark.django_db
def test_token_auth_user_active(data_fixture, user_schema_anonymous_client) -> None:
    user = data_fixture.create_user(email="janusz@cebula.com")
    user.set_password("test1234!")
    user.save()
    query = """
        mutation TokenAuth($email: String!, $password: String!) {
          tokenAuth(input: {email: $email, password: $password}){
            payload
          }
        }
        """

    result = user_schema_anonymous_client.execute(query, variables={"email": user.email, "password": "test1234!"})

    assert "errors" not in result
    assert result["data"] == ANY


@pytest.mark.django_db
def test_delete_cookie(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user(email="janusz@cebula.com")
    query = """
        mutation DeleteCookie{
          deleteAuthAndRefreshTokenCookie(input: {}) {
            deleted
          }
        }
        """

    user_schema_client.set_cookie(
        {
            jwt_settings.JWT_COOKIE_NAME: "1234",
            jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME: "4321",
        }
    )
    result = user_schema_client.execute(query, variables={"email": user.email, "password": "test1234!"})

    expected = {"deleteAuthAndRefreshTokenCookie": {"deleted": True}}
    assert "errors" not in result
    assert expected == result["data"]
