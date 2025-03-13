from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin
from django.core.validators import MaxLengthValidator, validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils import GrapheneModelMixin, TimeStampMixin
from users.manager import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampMixin, GrapheneModelMixin):
    firstname = models.CharField(
        _("first name"),
        max_length=150,
        blank=True,
        validators=[MaxLengthValidator(150)],
    )
    lastname = models.CharField(_("last name"), max_length=150, blank=True, validators=[MaxLengthValidator(150)])
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
        ),
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="users_user_set",
        related_query_name="users_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="users_user_set",
        related_query_name="users_user",
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        validators=[validate_email, MaxLengthValidator(150)],
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects: CustomUserManager = CustomUserManager()

    def __str__(self) -> str:
        return f"User({self.email=})"
