import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_login(register_client, client, login_client_data):
    login = reverse("login")

    response = client.post(login, login_client_data, format="json")
    assert response.status_code == 200
