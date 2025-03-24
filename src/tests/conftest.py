from typing import Any, Generator

import pytest
from django.contrib.auth.models import AnonymousUser
from faker import Faker
from graphene import Schema
from graphene.test import Client

from api.graphql.schema import schema as user_schema
from users.models import User


@pytest.fixture(scope="class", autouse=True)
def fake() -> Generator[Faker, Any, None]:
    yield Faker()


@pytest.fixture
def data_fixture(fake):
    from tests.fixtures import Fixtures

    return Fixtures(fake)


class UserSchemaClient:
    def __init__(self, schema: Schema, user: User | AnonymousUser | None = None) -> None:
        self.schema = schema
        self.user = user

    def execute(self, query: str, variables: dict[str, Any] | None = None):
        class TestContext:
            def __init__(self, user):
                self.user = user
                self.jwt_cookie = True

        context = TestContext(user=self.user)
        client = Client(self.schema, context_value=context)
        return client.execute(query, variable_values=variables)


@pytest.fixture
def user_schema_client(data_fixture) -> UserSchemaClient:
    user = data_fixture.create_user()
    return UserSchemaClient(user_schema, user=user)


@pytest.fixture
def user_schema_anonymous_client() -> UserSchemaClient:
    return UserSchemaClient(user_schema, user=AnonymousUser())
