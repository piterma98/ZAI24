from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils import TimeStampMixin


class PhonebookTypeEnum(models.TextChoices):
    personal = "personal"
    enterprise = "enterprise"


class PhonebookGroup(TimeStampMixin): ...


class PhonebookNumber(TimeStampMixin): ...


class Phonebook(TimeStampMixin):
    name = models.TextField(max_length=300)
    city = models.TextField()
    street = models.TextField()
    type = models.TextField(choices=PhonebookTypeEnum.choices)
    groups = models.ManyToManyField(
        PhonebookGroup,
        blank=True,
        help_text=_("Accounts to which user has access"),
        related_name="phonebooks",
    )
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
