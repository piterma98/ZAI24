import graphene
from graphql_relay import to_global_id

from api.graphql_utils import login_required
from users.models import User


class Me(graphene.ObjectType):
    id = graphene.ID()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

    def __init__(self, user: User) -> None:
        self.user = user

    def resolve_id(self, info: graphene.ResolveInfo) -> str:
        return to_global_id(f"{self.__class__.__name__}", self.user.id)

    def resolve_email(self, info: graphene.ResolveInfo) -> str:
        return self.user.email

    def resolve_first_name(self, info: graphene.ResolveInfo) -> str:
        return self.user.firstname

    def resolve_last_name(self, info: graphene.ResolveInfo) -> str:
        return self.user.lastname


class MeQuery(graphene.ObjectType):
    me = graphene.Field(Me)

    @login_required
    def resolve_me(self, info: graphene.ResolveInfo) -> Me:
        return Me(user=info.context.user)
