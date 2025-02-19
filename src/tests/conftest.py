import pytest
from django.contrib.auth import get_user_model
from nu_quran_api.apps.users.models import Category, Activity
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category", value=10)


@pytest.fixture
def activity(db, user, category):
    return Activity.objects.create(user=user, category=category)
