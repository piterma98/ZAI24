from graphene_django import DjangoObjectType

from phonebook.models import Phonebook


class PhonebookNode(DjangoObjectType):
    class Meta:
        model = Phonebook
        exclude = ("password",)
