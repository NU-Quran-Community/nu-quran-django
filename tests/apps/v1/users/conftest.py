import pytest
from django.core.management import call_command

from nu_quran_api.apps.v1.users.models import Activity, Category, User


@pytest.fixture(autouse=True, scope="function")
def load_data(db, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("flush", "--no-input")
        call_command("setuproles")


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpass",
        "first_name": "Test",
        "last_name": "User",
        "referrer": None,
        "supervisor": None,
        "groups": ["Student"],
    }


@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="Test Category", value=1)


@pytest.fixture
def activity(db, existing_user: User, category: Category) -> Activity:
    activity = Activity.objects.create(
        category=category, user=existing_user, date="2025-02-27T00:00:00Z"
    )
    return activity
