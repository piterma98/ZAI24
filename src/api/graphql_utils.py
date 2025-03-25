from typing import Callable, ParamSpec, TypeVar

import graphene
from graphql_relay import from_global_id

from api.exceptions import AuthenticationError, InputIdTypeMismatchError

P = ParamSpec("P")
T = TypeVar("T")

GraphqlMethod = Callable[P, T]


def login_required(func: GraphqlMethod) -> Callable[[GraphqlMethod], GraphqlMethod]:
    """
    Ensures that user with is_authenticated set to True can execute a mutation or resolver.

    The decorator works for any method that takes a ``ResolveInfo`` argument
    and looks for the user in context.
    """

    def resolve_or_mutate(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, graphene.ResolveInfo))
        if not info.context.user.is_authenticated:
            raise AuthenticationError()
        return func(*args, **kwargs)

    return resolve_or_mutate


def validate_gid(object_id: str, class_name: str) -> str:
    """
    Decode a global ID and raise InputIdTypeMismatchError if expected class does not match.
    """
    object_class_name, object_id = from_global_id(object_id)
    if object_class_name != class_name:
        raise InputIdTypeMismatchError(message=f"{object_id=} is not an {class_name}")
    return object_id
