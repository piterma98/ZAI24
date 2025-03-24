from app_auth.user_schema.mutations import Mutation as AuthMutation
from phonebook.user_schema.mutations import Mutation as PhonebookMutation
from users.user_schema.mutations import Mutation as UserMutation


class Mutation(AuthMutation, UserMutation, PhonebookMutation):
    pass
