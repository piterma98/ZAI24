import logging

import graphene
from graphene.relay.mutation import ClientIDMutation

from api.graphql_utils import login_required
from users.exceptions import ChangePasswordException, RegisterException
from users.handler import UserHandler
from users.user_schema.queries import UserNode

logger = logging.getLogger(__name__)


class RegisterSuccess(graphene.ObjectType):
    user = graphene.Field(UserNode)


class RegisterError(graphene.ObjectType):
    reason = graphene.String()


class RegisterResult(graphene.Union):
    class Meta:
        types = (RegisterSuccess, RegisterError)


class Register(ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        firstname = graphene.String(required=True)
        lastname = graphene.String(required=True)
        password = graphene.String(required=True)

    result = graphene.Field(RegisterResult)

    @classmethod
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        email: str,
        password: str,
        firstname: str,
        lastname: str,
    ) -> "Register":
        try:
            user = UserHandler().create_user(
                email=email,
                password=password,
                firstname=firstname,
                lastname=lastname,
            )
            return cls(result=RegisterSuccess(user=user))
        except RegisterException as e:
            return cls(result=RegisterError(reason=e.reason))


class ChangePasswordSuccess(graphene.ObjectType):
    message = graphene.String()


class ChangePasswordError(graphene.ObjectType):
    reason = graphene.String()


class ChangePasswordResult(graphene.Union):
    class Meta:
        types = (ChangePasswordSuccess, ChangePasswordError)


class ChangePassword(ClientIDMutation):
    class Input:
        new_password = graphene.String(required=True)
        old_password = graphene.String(required=True)

    result = graphene.Field(ChangePasswordResult)

    @classmethod
    @login_required
    def mutate_and_get_payload(
        cls,
        root,
        info: graphene.ResolveInfo,
        new_password: str,
        old_password: str,
    ) -> "ChangePassword":
        try:
            UserHandler().change_password(
                user_id=info.context.user.id,
                new_password=new_password,
                old_password=old_password,
            )
            return cls(result=ChangePasswordSuccess(message="Successfully changed password!"))
        except ChangePasswordException as e:
            return cls(result=ChangePasswordError(reason=e.reason))


class Mutation(graphene.ObjectType):
    register = Register.Field()
    change_password = ChangePassword.Field()
