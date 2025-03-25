import pytest

from users.models import User


@pytest.mark.django_db
def test_create_user_manager():
    user = User.objects.create_user("test@gmail.com", "password123")

    assert user.email == "test@gmail.com"
    assert user.check_password("password123")
    assert user.is_staff is False
    assert user.is_staff is False


@pytest.mark.django_db
def test_create_superuser_manager():
    user = User.objects.create_superuser("test@gmail.com", "password123")

    assert user.email == "test@gmail.com"
    assert user.check_password("password123")
    assert user.is_staff is True
    assert user.is_staff is True


@pytest.mark.django_db
def test_create_superuser_manager_errors():
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser("test@gmail.com", "password123", is_staff=False)

    with pytest.raises(ValueError, match="Superuser must have is_superuser=True."):
        User.objects.create_superuser("test@gmail.com", "password123", is_superuser=False)
