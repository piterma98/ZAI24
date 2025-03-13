import graphene
from graphene_django import DjangoObjectType

from api.graphql_utils import login_required
from users.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = (
            "password",
            "current_account",
            "groups",
            "account_set",
            "accounts",
            "new_email",
        )
        interfaces = (graphene.relay.Node,)

    is_owner = graphene.Boolean()

    @login_required
    def resolve_is_owner(self, info: graphene.ResolveInfo) -> bool:
        return self == info.context.user.current_account.owner
