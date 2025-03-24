from graphene.relay import Node

from phonebook.user_schema.queries import Query as PhonebookQuery
from users.user_schema.me import MeQuery


class Query(MeQuery, PhonebookQuery):
    node = Node.Field()
