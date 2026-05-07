import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import MyUser as User
from ..models import Task


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


@pytest.fixture
def other_user():
    other_user = User.objects.create_user(
        username="ali", password="alimad70040", email="ali@gmail.com"
    )
    return other_user


@pytest.fixture
def common_task(common_user):
    task = Task.objects.create(user=common_user.profile, title="test")
    return task


@pytest.fixture
def other_user_task(other_user):
    return Task.objects.create(user=other_user.profile, title="test")


@pytest.mark.django_db
class TestToDoAPi:

    def test_todo_list_response_200_status(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_todo_list_response_401_status(self, api_client):
        url = reverse("Task-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_create_task_201_status(self, api_client, common_user):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-list")
        data = {"title": "test"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Task.objects.filter(
            user=common_user.profile, title=data["title"]
        ).exists()

    def test_create_task_401_status(self, api_client):
        url = reverse("Task-list")
        data = {"title": "test"}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_todo_detail_response_200_status(
        self, api_client, common_user, common_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_todo_detail_put_response_200_status(
        self, api_client, common_user, common_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        data = {"title": "test"}
        response = api_client.put(url, data)
        assert response.status_code == 200

    def test_todo_detail_response_400_status(
        self, api_client, common_user, common_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        data = {}
        response = api_client.put(url, data)
        assert response.status_code == 400

    def test_task_detail_get_response_401_status(self, api_client, common_task):
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_todo_detail_response_401_status(self, api_client, common_task):
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        data = {"title": "test"}
        response = api_client.put(url, data)
        assert response.status_code == 401

    def test_task_detail_delete_response_401_status(self, api_client, common_task):
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_task_detail_response_204_status(
        self, api_client, common_user, common_task
    ):

        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": common_task.pk})
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_user_can_not_access_to_other_users_task(
        self, api_client, common_user, other_user_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": other_user_task.pk})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_user_can_not_update_other_users_task(
        self, api_client, common_user, other_user_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": other_user_task.pk})
        data = {"title": "test"}
        response = api_client.put(url, data)
        assert response.status_code == 404

    def test_user_can_not_delete_other_users_task(
        self, api_client, common_user, other_user_task
    ):
        api_client.force_authenticate(user=common_user)
        url = reverse("Task-detail", kwargs={"pk": other_user_task.pk})
        data = {"title": "test"}
        response = api_client.delete(url, data)
        assert response.status_code == 404
