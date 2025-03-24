from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from model_utils import TimeStampMixin


class PhonebookEntryTypeEnum(models.TextChoices):
    personal = "personal"
    enterprise = "enterprise"


class PhonebookGroup(TimeStampMixin):
    name = models.TextField(max_length=50, validators=[MaxLengthValidator(50)], unique=True)

    def __str__(self) -> str:
        return f"PhonebookGroup({self.name=})"


class PhonebookNumber(TimeStampMixin):
    number = models.TextField(max_length=20, null=True, validators=[MaxLengthValidator(20)])


class PhonebookEntry(TimeStampMixin):
    name = models.TextField(max_length=300, validators=[MaxLengthValidator(300)])
    city = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    street = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    postal_code = models.TextField(max_length=50, validators=[MaxLengthValidator(50)])
    type = models.TextField(choices=PhonebookEntryTypeEnum.choices)
    groups = models.ManyToManyField(
        PhonebookGroup,
        blank=True,
        help_text=_("Group that phone entry belongs"),
        related_name="phonebook_entries",
    )
    numbers = models.ManyToManyField(
        PhonebookNumber,
        blank=True,
        help_text=_("Numbers associated with phonebook entry"),
        related_name="phonebook_entries",
    )
    created_by = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)

    # class Meta:
    #     ordering = ["-created_at"]
