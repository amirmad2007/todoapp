import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import MyUser as User


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        username="amir",
        password="amirmad2007",
        email="amirmadani901@gmail.com",
    )
    return user


@pytest.mark.django_db
class TestUserApi:

    def test_register_response_400_status(self, api_client):

        url = reverse("register_user")
        data = {
            "username": "string",
            "email": "user@example.com",
            "password": "123",
            "confirm_password": "123",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_register_response_201_status(self, api_client):

        url = reverse("register_user")
        data = {
            "username": "amirmad2007",
            "email": "user@example.com",
            "password": "amirmad2007",
            "confirm_password": "amirmad2007",
        }
        response = api_client.post(url, data)
        assert response.status_code == 201

    def test_register_response_403_status(self, common_user, api_client):
        api_client.force_authenticate(common_user)
        url = reverse("register_user")
        data = {
            "username": "amirmad2007",
            "email": "user@example.com",
            "password": "amirmad2007",
            "confirm_password": "amirmad2007",
        }
        response = api_client.post(url, data)
        assert response.status_code == 403

    def test_change_password_response_400_status(self, common_user, api_client):
        api_client.force_authenticate(common_user)
        url = reverse("change-password")
        data = {
            "old_password": "amirmad2007",
            "password": "amirmad2007",
            "confirm_password": "amirmad2007",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_change_password_response_200_status(self, common_user, api_client):
        api_client.force_authenticate(common_user)
        url = reverse("change-password")
        data = {
            "old_password": "amirmad2007",
            "password": "amirmadani",
            "confirm_password": "amirmadani",
        }
        response = api_client.post(url, data)
        assert response.status_code == 200

    def test_change_password_response_401_status(self, api_client):
        url = reverse("change-password")
        data = {
            "old_password": "amirmad2007",
            "password": "amirmadani",
            "confirm_password": "amirmadani",
        }
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_request_to_reset_password_403_status(self, common_user, api_client):
        api_client.force_authenticate(common_user)
        url = reverse("request_to_rest_password")
        response = api_client.post(url)
        assert response.status_code == 403

    def test_request_to_reset_password_400_status(self, api_client):
        url = reverse("request_to_rest_password")
        response = api_client.post(url)
        assert response.status_code == 400

    def test_request_to_reset_password_200_status(self, api_client, common_user):
        url = reverse("request_to_rest_password")
        data = {"email": common_user.email}
        response = api_client.post(url, data)
        assert response.status_code == 200

    def test_resend_verification_403_status(self, common_user, api_client):
        api_client.force_authenticate(common_user)
        url = reverse("resend_verification")
        response = api_client.post(url)
        assert response.status_code == 403

    def test_resend_verification_400_status(self, api_client):
        url = reverse("resend_verification")
        response = api_client.post(url)
        assert response.status_code == 400

    def test_resend_verification_200_status(self, api_client, common_user):
        url = reverse("resend_verification")
        data = {"email": common_user.email}
        response = api_client.post(url, data)
        assert response.status_code == 200

    def test_profile_response_200_status(self, api_client, common_user):
        api_client.force_authenticate(common_user)
        url = reverse("profile")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_profile_response_401_status(self, api_client):
        url = reverse("profile")
        response = api_client.get(url)
        assert response.status_code == 401
