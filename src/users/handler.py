import logging

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from users.exceptions import (
    ChangePasswordException,
    IncorrectPasswordError,
    RegisterException,
    SamePasswordError,
    UpdateUserException,
)
from users.models import User

logger = logging.getLogger(__name__)


class UserHandler:
    @transaction.atomic
    def create_user(self, email: str, password: str, firstname: str, lastname: str) -> User:
        if User.objects.filter(email=email).exists():
            logger.error("User with given email already exists!")
            raise RegisterException(reason="User with given email already exists!")
        try:
            user = User(
                email=email,
                firstname=firstname,
                lastname=lastname,
            )
            user.set_password(password)
            user.full_clean()
            user.save()
        except (ValidationError, IntegrityError, ValueError) as e:
            logger.error(f"Failed to create user {e}")
            raise RegisterException(reason="Failed to create user") from e
        return user

    @transaction.atomic
    def update_user(
        self,
        user_id: int,
        firstname: str | None = None,
        lastname: str | None = None,
    ) -> User:
        user_fields_to_update: list[str] = []
        try:
            user = User.objects.get(id=user_id)
            if firstname:
                user.firstname = firstname
                user_fields_to_update.append("firstname")
            if lastname:
                user.lastname = lastname
                user_fields_to_update.append("lastname")
        except (User.DoesNotExist, ValueError, ValidationError) as e:
            logger.warning(f"Error while updating user {e}")
            raise UpdateUserException(reason="Error while updating user!") from e
        user.save(update_fields=user_fields_to_update)
        return user

    @transaction.atomic
    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> None:
        try:
            user = User.objects.get(id=user_id)
            user.change_password(old_password=old_password, new_password=new_password)
            user.save()
        except (User.DoesNotExist, ValueError) as e:
            logger.error(f"Error while changing password {e}")
            raise ChangePasswordException(reason="Error while changing password")
        except SamePasswordError:
            raise ChangePasswordException(reason="New password is the same as old password")
        except IncorrectPasswordError:
            raise ChangePasswordException(reason="Old password is incorrect")
        logger.info(f"Successfully changed password for {user=}")
