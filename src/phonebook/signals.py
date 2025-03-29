from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from phonebook.models import PhonebookEntry


@receiver(pre_save, sender=PhonebookEntry)
def phonebook_pre_save(sender, instance: PhonebookEntry, *args, **kwargs) -> None:
    if not instance.slug:
        instance.slug = slugify(instance.name)
