import graphene
from graphene.relay import Node


class Query(graphene.ObjectType):
    node = Node.Field()
