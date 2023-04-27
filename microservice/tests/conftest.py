import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def not_client_data():
    data = {
        "security_question": "question",
        "security_answer": "answer",
        "email": "vlad.sergienko00@yandex.ru",
        "client_id": {
            "mobile_phone": "9311111151",
            "first_name": "string",
            "middle_name": "string",
            "last_name": "string",
            "password": "passWorD1",
            "accession_date": "2000-10-10",
            "country_of_residence": "True",
        },
        "passport_from_client": {"passport_number": "0000000029", "birth_date": "2000-10-10"},
    }

    return data


@pytest.fixture
def client_data():
    data = {
        "security_question": "question",
        "security_answer": "answer",
        "email": "vlad.sergienko00@yandex.ru",
        "client_id": {"password": "passWorD1", "mobile_phone": "9311111151"},
        "passport_from_client": {"passport_number": "0000000029", "birth_date": "2000-10-10"},
    }

    return data


@pytest.fixture
def register_client(not_client_data, client):
    sign_up_url = reverse("sign_up_not_client")
    response = client.post(sign_up_url, not_client_data, format="json")
    return response


@pytest.fixture
def make_client_active(client, register_client, client_data):
    sign_up_client_url = reverse("sign_up_client")
    response = client.patch(sign_up_client_url, client_data, format="json")
    return response


@pytest.fixture
def login_client_data():
    data = {
        "Login": "9311111151",
        "Password": "passWorD1",
    }
    return data


@pytest.fixture
def login(register_client, client, login_client_data):
    login = reverse("login")
    response = client.post(login, login_client_data)
    return response.data


@pytest.fixture
def client_data_with_email():
    data = {
        "Login": "9311111151",
        "Password": "passWorD1",
        "Email": "vlad.sergienko00@yandex.ru",
    }
    return data
