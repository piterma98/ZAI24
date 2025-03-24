import pytest

from users.exceptions import ChangePasswordException, RegisterException
from users.handler import UserHandler
from users.models import User


@pytest.mark.django_db
def test_user_handler_create_user() -> None:
    email = "foo@bar.com"
    password = "foobar1@34"
    firstname = "Gandalf"
    lastname = "Grey"

    user = UserHandler().create_user(
        email=email,
        password=password,
        firstname=firstname,
        lastname=lastname,
    )

    assert user.email == email
    assert user.firstname == firstname
    assert user.lastname == lastname
    assert User.objects.all().count() == 1


@pytest.mark.django_db
def test_user_handler_update_user(data_fixture) -> None:
    user = data_fixture.create_user(
        email="janusz@cebula.com",
        firstname="Janusz",
        lastname="Tracz",
    )
    firstname = "Gandalf"
    lastname = "Grey"

    UserHandler().update_user(
        user_id=user.id,
        firstname=firstname,
        lastname=lastname,
    )

    user.refresh_from_db()
    assert user.firstname == firstname
    assert user.lastname == lastname


@pytest.mark.django_db
def test_user_handler_user_already_exists(data_fixture) -> None:
    data_fixture.create_user(
        email="janusz@cebula.com",
        firstname="Janusz",
        lastname="Tracz",
    )
    email = "janusz@cebula.com"
    firstname = "Gandalf"
    lastname = "Grey"

    with pytest.raises(RegisterException) as e:
        UserHandler().create_user(
            email=email,
            password="password",
            firstname=firstname,
            lastname=lastname,
        )

    assert e.value.reason == "User with given email already exists!"


@pytest.mark.django_db
def test_change_password_user_does_not_exist() -> None:
    with pytest.raises(ChangePasswordException) as e:
        UserHandler().change_password(old_password="testing123", new_password="testing2", user_id=1)

    assert e.value.reason == "Error while changing password"


@pytest.mark.django_db
def test_change_password_incorrect_password(data_fixture) -> None:
    user = data_fixture.create_user(
        email="janusz@cebula.com",
        firstname="Janusz",
        lastname="Tracz",
    )
    user.set_password("testing")
    user.save()

    with pytest.raises(ChangePasswordException) as e:
        UserHandler().change_password(old_password="testing123", new_password="testing2", user_id=user.id)

    assert e.value.reason == "Old password is incorrect"


@pytest.mark.django_db
def test_change_password_same_password(data_fixture) -> None:
    user = data_fixture.create_user(
        email="janusz@cebula.com",
        firstname="Janusz",
        lastname="Tracz",
    )
    user.set_password("testing")
    user.save()

    with pytest.raises(ChangePasswordException) as e:
        UserHandler().change_password(old_password="testing", new_password="testing", user_id=user.id)

    assert e.value.reason == "New password is the same as old password"
