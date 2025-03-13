from graphene.relay import Node

from users.user_schema.me import MeQuery


class Query(MeQuery):
    node = Node.Field()
