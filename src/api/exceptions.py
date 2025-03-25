from graphql import GraphQLError


class AuthenticationError(GraphQLError):
    """
    Signals  that request is unauthenticated.

    The only message is class name to avoid exposing sensitive information
    in `errors` field of the GraphQL response.
    """

    def __init__(self):
        super().__init__(message=self.__class__.__name__)


class InputIdTypeMismatchError(GraphQLError):
    pass
