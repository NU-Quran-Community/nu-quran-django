import pytest
from nu_quran_api.apps.users.models import User, Category, Activity


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", password="testpass")
    assert user.username == "testuser"
    assert user.check_password("testpass")


@pytest.mark.django_db
def test_create_category():
    category = Category.objects.create(name="Test Category", value=10)
    assert category.name == "Test Category"
    assert category.value == 10


@pytest.mark.django_db
def test_create_activity(user, category):
    activity = Activity.objects.create(user=user, category=category)
    assert activity.user == user
    assert activity.category == category


@pytest.mark.django_db
def test_str_methods(user, category, activity):
    assert str(category) == "Test Category"
    assert str(activity) == f"{user} - {category} - {activity.date}"
