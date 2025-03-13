import graphene
from graphql_jwt.relay import ObtainJSONWebToken, Refresh
from graphql_jwt.settings import jwt_settings


class DeleteRefreshAndAuthTokenCookie(graphene.ClientIDMutation):
    deleted = graphene.Boolean(required=True)

    @classmethod
    def delete_cookie(cls, root, info: graphene.ResolveInfo, **kwargs) -> "DeleteRefreshAndAuthTokenCookie":
        context = info.context
        context.delete_jwt_cookie = jwt_settings.JWT_COOKIE_NAME in context.COOKIES and getattr(
            context, "jwt_cookie", False
        )
        context.delete_refresh_token_cookie = jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME in context.COOKIES and getattr(
            context, "jwt_cookie", False
        )
        return cls(deleted=context.delete_refresh_token_cookie)

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)


class Mutation(graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()
    refresh_token = Refresh.Field()
    delete_auth_and_refresh_token_cookie = DeleteRefreshAndAuthTokenCookie.Field()
