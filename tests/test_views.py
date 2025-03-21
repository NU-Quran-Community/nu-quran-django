import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserAPI:
    def test_get_user_details(self, client: APIClient, existing_user, jwt_admin_token):
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
        self, client, existing_user, jwt_admin_token, admin_user
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        data = {"username": "updated_username", "user": existing_user.id}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_user(self, client, jwt_admin_token, existing_user):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.delete(f"/users/{existing_user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_cannot_update_other_users(
        self, client, existing_user, jwt_user_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        data = {"groups": ["Admin"]}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_other_users(
        self, client, existing_user, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "deleted_user"}
        response = client.delete(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_user_cannot_update_other_users(
        self, client, existing_user, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "updated_user"}
        response = client.patch(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_supervisor_user_cannot_delete_other_users(
        self, client, existing_user, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        data = {"username": "delete_user"}
        response = client.delete(f"/users/{existing_user.id}/", data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestUserActivityPermissions:
    def test_user_can_list_activities(self, client, existing_user, jwt_user_token):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_user_cannot_modify_activity(self, client, jwt_user_token, activity):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        data = {"category": activity.category.id, "user": activity.user.id}
        response = client.patch(
            f"/users/{activity.user.id}/activities/{activity.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_cannot_delete_activity(
        self, client, existing_user, jwt_user_token, activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_user_token}")
        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestSupervisorActivityPermissions:
    def test_supervisor_can_list_activities(
        self, client, existing_user, jwt_supervisor_token
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_supervisor_can_modify_activity(
        self, client, supervisor_user, jwt_supervisor_token, activity
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
        self, client, supervisor_user, jwt_supervisor_token, activity
    ):
        activity.user.supervisor = supervisor_user
        activity.user.save()
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_supervisor_token}")

        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestAdminActivityPermissions:
    def test_admin_can_list_activities(self, client, jwt_admin_token, existing_user):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.get(f"/users/{existing_user.id}/activities/")
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_modify_activity(self, client, jwt_admin_token, activity):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        data = {"category": activity.category.id, "user": activity.user.id}
        response = client.patch(
            f"/users/{activity.user.id}/activities/{activity.id}/", data, format="json"
        )
        assert response.status_code == status.HTTP_200_OK

    def test_admin_can_delete_activity(self, client, jwt_admin_token, activity):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response = client.delete(f"/users/{activity.user.id}/activities/{activity.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserPointsAPI:
    def test_get_all_users_points(
        self, client: APIClient, existing_user, admin_user, activity, jwt_admin_token
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
        self, client: APIClient, jwt_admin_token, existing_user, activity
    ):
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_admin_token}")
        response: Response = client.get(f"/users/{existing_user.id}/points/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["user"] == existing_user.id
        assert "points" in response.data
        assert "activities" in response.data

    def test_get_user_points_no_activities(
        self, client: APIClient, jwt_admin_token, existing_user
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
