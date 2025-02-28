import pytest
from django.contrib.auth.models import Group
from nu_quran_api.apps.users.models import User, Activity, Category
from django.core.management import call_command
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def jwt_admin_token(admin_user) -> str:
    token = AccessToken.for_user(admin_user)
    return str(token)


@pytest.fixture
def jwt_user_token(existing_user) -> str:
    token = AccessToken.for_user(existing_user)
    return str(token)


@pytest.fixture
def jwt_supervisor_token(supervisor_user) -> str:
    token = AccessToken.for_user(supervisor_user)
    return str(token)


@pytest.fixture(autouse=True, scope="function")
def load_data(db, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("setuproles")
        call_command("loaddata", "category.json")


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
def existing_user(db):
    group, _ = Group.objects.get_or_create(name="Student")
    user = User.objects.create_user(
        email="existinguser@example.com",
        username="existinguser",
        password="testpass",
        first_name="Existing",
        last_name="User",
    )
    user.groups.add(group)
    return user


@pytest.fixture
def admin_user(db):
    group = Group.objects.get(name="Admin")
    admin = User.objects.create_user(
        email="admin@example.com",
        username="adminuser",
        password="adminpass",
        first_name="Admin",
        last_name="User",
    )
    admin.groups.add(group)
    return admin


@pytest.fixture
def supervisor_user(db):
    group, _ = Group.objects.get_or_create(name="Supervisor")
    supervisor = User.objects.create_user(
        email="supervisor@example.com",
        username="supervisoruser",
        password="supervisorpass",
        first_name="Supervisor",
        last_name="User",
    )
    supervisor.groups.add(group)
    return supervisor


@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="Test Category", value=1)


@pytest.fixture
def activity(db, existing_user, category) -> Activity:
    activity = Activity.objects.create(
        category=category, user=existing_user, date="2025-02-27"
    )
    return activity
