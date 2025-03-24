import pytest

from users.models import User


@pytest.mark.django_db
def test_register(
    user_schema_anonymous_client,
) -> None:
    email = "foo@bar.com"
    password = "foobar1@34"
    firstname = "Gandalf"
    lastname = "Grey"
    query = """
        mutation register($email: String!, $password: String!, $firstname: String!, $lastname: String!) {
          register(
            input: {email: $email, password: $password, firstname: $firstname, lastname: $lastname}
          ) {
            result {
              ... on RegisterSuccess {
                user {
                  email
                  firstname
                  lastname
                }
              }
              ... on RegisterError{
                reason
              }
            }
          }
        }
        """
    variables = {
        "password": password,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
    }
    expected_result = {
        "register": {
            "result": {
                "user": {
                    "email": "foo@bar.com",
                    "firstname": "Gandalf",
                    "lastname": "Grey",
                }
            }
        }
    }

    result = user_schema_anonymous_client.execute(query, variables=variables)

    assert "errors" not in result
    assert result["data"] == expected_result
    created_user = User.objects.get(email=email)
    assert created_user.email == email
    assert created_user.firstname == firstname
    assert created_user.lastname == lastname
    assert created_user.is_active is True


@pytest.mark.django_db
def test_change_user_password(data_fixture, user_schema_client) -> None:
    user = data_fixture.create_user(email="user@gmail.com")
    new_password = "NewPassword1234!"
    old_password = "OldPassword1234!"
    user.set_password(old_password)
    user.save()
    user_schema_client.user = user
    query = """
            mutation changeUserPassword($oldPassword: String!, $newPassword: String!) {
              changePassword(
                input: {oldPassword: $oldPassword, newPassword: $newPassword}
              ) {
                result {
                  ... on ChangePasswordSuccess {
                    message
                  }
                }
              }
            }
            """
    variables = {
        "oldPassword": old_password,
        "newPassword": new_password,
    }
    expected_result = {"changePassword": {"result": {"message": "Successfully changed password!"}}}

    result = user_schema_client.execute(query, variables=variables)

    user.refresh_from_db()
    assert "errors" not in result
    assert result["data"] == expected_result
    assert user.check_password(new_password)
    assert user.check_password(old_password) is False
