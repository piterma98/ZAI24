from tests.fixtures.user import UserFixture


class Fixtures(UserFixture):
    def __init__(self, fake=None) -> None:
        self.fake = fake
