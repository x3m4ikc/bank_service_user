import time

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_email_verify(register_client, client, client_data_with_email, snapshot):
    login = reverse("login")
    login_data = {
        "Login": client_data_with_email["Login"],
        "Password": client_data_with_email["Password"],
    }
    response = client.post(login, login_data, format="json")
    token = response.data["access_token"]
    client.credentials(HTTP_AUTHORIZATION=token)

    verify_url = reverse("email_verify")
    response = client.put(verify_url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["email"], client_data_with_email["Email"])

    # Повторный запрос с истечением времени

    time.sleep(30)
    response = client.patch(verify_url)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["email"], client_data_with_email["Email"])

    # Повторный запрос без ожидания времени

    response = client.patch(verify_url)
    assert response.status_code == status.HTTP_406_NOT_ACCEPTABLE
