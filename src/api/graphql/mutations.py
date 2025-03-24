from app_auth.user_schema.mutations import Mutation as AuthMutation
from users.user_schema.mutations import Mutation as UserMutation


class Mutation(AuthMutation, UserMutation):
    pass
