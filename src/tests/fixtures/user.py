from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()


class UserFixture:
    fake: Faker

    def create_user(self, **kwargs):
        if "email" not in kwargs:
            kwargs["email"] = self.fake.unique.email()
        if "firstname" not in kwargs:
            kwargs["firstname"] = self.fake.first_name()
        if "lastname" not in kwargs:
            kwargs["lastname"] = self.fake.last_name()
        if "password" not in kwargs:
            kwargs["password"] = "password"

        user = User(**kwargs)
        user.set_password(kwargs["password"])
        user.save()

        return user
