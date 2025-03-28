from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils import GrapheneModelMixin, TimeStampMixin


class PhonebookEntryTypeEnum(models.TextChoices):
    personal = "personal"
    enterprise = "enterprise"


class PhonebookNumberTypeEnum(models.TextChoices):
    mobile = "mobile"
    landline = "landline"


class PhonebookGroup(TimeStampMixin):
    name = models.TextField(max_length=50, validators=[MaxLengthValidator(50)], unique=True)

    def __str__(self) -> str:
        return f"PhonebookGroup({self.name=})"


class PhonebookEntry(TimeStampMixin, GrapheneModelMixin):
    name = models.TextField(max_length=300, validators=[MaxLengthValidator(300)])
    city = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    street = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    postal_code = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    country = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    type = models.TextField(choices=PhonebookEntryTypeEnum.choices)
    groups = models.ManyToManyField(
        PhonebookGroup,
        blank=True,
        help_text=_("Group that phone entry belongs"),
        related_name="phonebook_entries",
    )
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    phonebook_number: models.QuerySet["PhonebookNumber"]

    def __str__(self) -> str:
        return f"PhonebookEntry({self.name=})"


class PhonebookNumber(TimeStampMixin, GrapheneModelMixin):
    phonebook_entry = models.ForeignKey(PhonebookEntry, on_delete=models.CASCADE, related_name="phonebook_number")
    number = models.TextField(max_length=20, null=True, validators=[MaxLengthValidator(20)])
    type = models.TextField(choices=PhonebookNumberTypeEnum.choices)

    def __str__(self) -> str:
        return f"PhonebookNumber({self.phonebook_entry=}, {self.number=}, {self.type=})"


class PhonebookEntryRating(TimeStampMixin, GrapheneModelMixin):
    phonebook_entry = models.ForeignKey(PhonebookEntry, on_delete=models.CASCADE, related_name="phonebook_rating")
    rate = models.PositiveIntegerField()
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f"PhonebookNumberRating({self.phonebook_entry=}, {self.rate=}, {self.created_by})"
