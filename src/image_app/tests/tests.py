from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from image_app.models import Image

test_username = "test_user"
test_password = "test_password"


@pytest.fixture
def image():
    return Image.objects.create()


@pytest.fixture
def images():
    images = [Image() for _ in range(5)]
    return Image.objects.bulk_create(images)


@pytest.fixture
def user() -> User:
    user = User.objects.create_user(username=test_username, password=test_password)
    return user


@pytest.fixture
def token(user: User, client: APIClient):
    response = client.post(
        reverse("token_obtain_pair"),
        {"username": user.username, "password": test_password},
    )
    return response.data["access"]


@pytest.mark.django_db
def test_upload_image(client: APIClient, token: str):
    with open("image_app/tests/cat.jpeg", "rb") as image_file:
        response = client.post(
            reverse("images"),
            {"image": image_file},
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_list_images(client: APIClient, token: str, images: list[Image]):
    response = client.get(reverse("images"), HTTP_AUTHORIZATION=f"Bearer {token}")
    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_get_image(client: APIClient, token: str, image: Image):
    response = client.get(
        reverse("image", args=[image.pk]), HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 200
    assert response.data["status"] == "In progress"
    assert response.data["upload_date"] == datetime.now().date().strftime("%Y-%m-%d")


@pytest.mark.django_db
def test_update_image(client: APIClient, token: str, image: Image):
    url = reverse("image", args=[image.pk])
    response = client.patch(
        url,
        HTTP_AUTHORIZATION=f"Bearer {token}",
        data={"name": "Image"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.data["name"] == "Image"


@pytest.mark.django_db
def test_delete_image(client: APIClient, token: str, image: Image):
    response = client.delete(
        reverse("image", args=[image.pk]), HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 204
    assert response.data is None
    response = client.get(
        reverse("image", args=[image.pk]), HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    assert response.status_code == 404
