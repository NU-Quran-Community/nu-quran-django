from datetime import timedelta

import pytest
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from nu_quran_api.apps.users.models import Activity, Category, User


@pytest.mark.django_db
class TestUserAPI:
    def test_get_user_details(
        self, client: APIClient, existing_user: User, jwt_admin_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(f"/users/{existing_user.id}/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["username"] == existing_user.username

    def test_get_nonexistent_user(self, client: APIClient, jwt_admin_token):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get("/users/999/")
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestUserPermissions:

    def test_admin_can_list_users(self, client, jwt_admin_token):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.get("/users/")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_update_user(
        self, client, existing_user: User, jwt_admin_token, admin_user
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        data = {"username": "updated_username", "user": existing_user.id}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_user(self, client, jwt_admin_token, existing_user: User):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.delete(f"/users/{existing_user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_cannot_update_other_users(
        self, client, existing_user: User, jwt_user_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        data = {"groups": ["Admin"]}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_other_users(
        self, client, existing_user: User, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "deleted_user"}
        response = client.delete(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_user_cannot_update_other_users(
        self, client, existing_user: User, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "updated_user"}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_user_cannot_delete_other_users(
        self, client, existing_user: User, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "delete_user"}
        response = client.delete(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserActivityPermissions:
    def test_user_can_list_activities(
        self, client, existing_user: User, jwt_user_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_modify_activity(
        self, client, jwt_user_token, activity: Activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        data = {"category": activity.category.id, "user": activity.user.id}
        response = client.patch(
            f"/users/{activity.user.id}/activities/{activity.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_activity(
        self, client, existing_user: User, jwt_user_token, activity: Activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSupervisorActivityPermissions:
    def test_supervisor_can_list_activities(
        self, client, existing_user: User, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_supervisor_can_modify_activity(
        self, client, supervisor_user, jwt_supervisor_token, activity: Activity
    ):
        activity.user.supervisor = supervisor_user
        activity.user.save()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")

        data = {"category": activity.category.id, "user": activity.user.id}
        response = client.patch(
            f"/users/{activity.user.id}/activities/{activity.id}/", data, format="json"
        )

        assert response.status_code == status.HTTP_200_OK

    def test_supervisor_can_delete_activity(
        self, client, supervisor_user, jwt_supervisor_token, activity: Activity
    ):
        activity.user.supervisor = supervisor_user
        activity.user.save()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")

        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestAdminActivityPermissions:
    def test_admin_can_list_activities(
        self, client, jwt_admin_token, existing_user: User
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_modify_activity(
        self, client, jwt_admin_token, activity: Activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        data = {"category": activity.category.id, "user": activity.user.id}
        response = client.patch(
            f"/users/{activity.user.id}/activities/{activity.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_activity(
        self, client, jwt_admin_token, activity: Activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserPointsAPI:
    def test_get_all_users_points(
        self,
        client: APIClient,
        existing_user: User,
        admin_user,
        activity: Activity,
        jwt_admin_token,
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.get("/users/points/")
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {"user": existing_user.id, "points": 1, "activities": [activity.id]},
                {"user": admin_user.id, "points": 0, "activities": []},
            ],
        }
        assert response.status_code == status.HTTP_200_OK
        assert response.data == expected_data

    def test_get_user_points_by_id(
        self,
        client: APIClient,
        jwt_admin_token,
        existing_user: User,
        activity: Activity,
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(f"/users/{existing_user.id}/points/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert User.objects.filter(
            id=existing_user.id
        ).exists(), "User does not exist in test DB"
        assert "points" in response.data
        assert "activities" in response.data

    def test_get_user_points_no_activities(
        self, client: APIClient, jwt_admin_token, existing_user: User
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(f"/users/{existing_user.id}/points/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert response.data["points"] == 0
        assert list(response.data["activities"]) == []

    def test_get_nonexistent_user_points(self, client: APIClient, jwt_admin_token):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get("/users/999999/points/")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_filter_user_points_by_category(
        self,
        client,
        jwt_admin_token,
        existing_user: User,
        category: Category,
        activity: Activity,
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(
            f"/users/{existing_user.id}/points/?category={category.id}"
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert "points" in response.data
        assert "activities" in response.data

    def test_filter_user_points_by_date_range(
        self,
        client,
        jwt_admin_token,
        existing_user: User,
        category: Category,
        activity: Activity,
    ):
        past_activity = Activity.objects.create(
            user=existing_user,
            category=category,
            date=(now() - timedelta(days=10)).strftime("%Y-%m-%dT00:00:00Z"),
        )
        future_activity = Activity.objects.create(
            user=existing_user,
            category=category,
            date=(now() + timedelta(days=10)).strftime("%Y-%m-%dT00:00:00Z"),
        )

        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(
            f"/users/{existing_user.id}/points/?date_after={(now() - timedelta(days=5)).strftime('%Y-%m-%d')}&date_before={(now() + timedelta(days=5)).strftime('%Y-%m-%d')}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert past_activity.id not in response.data["activities"]
        assert future_activity.id not in response.data["activities"]

    def test_filter_user_points_by_category_and_date(
        self,
        client,
        jwt_admin_token,
        existing_user: User,
        activity: Activity,
        category: Category,
    ):
        today = now().date()
        category2 = Category.objects.create(name="Test 2", value=5, name_ar="تجربه")
        valid_activity = Activity.objects.create(
            user=existing_user,
            category=category,
            date=today.strftime("%Y-%m-%dT00:00:00Z"),
        )
        invalid_activity = Activity.objects.create(
            user=existing_user,
            category=category2,
            date=today.strftime("%Y-%m-%dT00:00:00Z"),
        )

        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.get(
            f"/users/{existing_user.id}/points/?category={category.id}&date_after={(today - timedelta(days=5)).strftime('%Y-%m-%d')}&date_before={today.strftime('%Y-%m-%d')}"
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert valid_activity.id in response.data["activities"]
        assert invalid_activity.id not in response.data["activities"]
