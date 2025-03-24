from tests.fixtures.phonebook import PhonebookFixture
from tests.fixtures.user import UserFixture


class Fixtures(UserFixture, PhonebookFixture):
    def __init__(self, fake=None) -> None:
        self.fake = fake
