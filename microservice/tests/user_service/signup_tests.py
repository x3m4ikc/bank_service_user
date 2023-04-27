import json

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_sign_up_not_client(client, not_client_data, snapshot):
    sign_up_url = reverse("sign_up_not_client")

    response = client.post(sign_up_url, not_client_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    snapshot.assert_match(response.data["email"], not_client_data["email"])
    snapshot.assert_match(
        response.data["client_id"]["mobile_phone"], not_client_data["client_id"]["mobile_phone"]
    )


@pytest.mark.django_db
def test_reset_password(client, register_client, not_client_data, snapshot):
    phone = register_client.data["client_id"]["mobile_phone"]
    reset_password_url = reverse("reset_password")
    reset_password_url_with_params = f"{reset_password_url}?mobile_phone={phone}"
    response = client.patch(reset_password_url_with_params, {"new_password": "sdgsddsf"})
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(
        response.data["client"]["first_name"], not_client_data["client_id"]["first_name"]
    )


@pytest.mark.django_db
def test_sign_up_client(client, client_data, not_client_data, snapshot):
    sign_up_url = reverse("sign_up_not_client")
    response = client.post(sign_up_url, not_client_data, format="json")
    sign_up_client_url = reverse("sign_up_client")
    response = client.patch(sign_up_client_url, client_data, format="json")

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["email"], client_data["email"])
    snapshot.assert_match(
        response.data["client_id"]["mobile_phone"], client_data["client_id"]["mobile_phone"]
    )


@pytest.mark.django_db
def test_reset_security_question(make_client_active, client, login_client_data, snapshot):
    login = reverse("login")
    login_response = client.post(login, login_client_data, format="json")
    reset_question_url = reverse("reset_security_question")
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['access_token']}")
    response = client.patch(
        reset_question_url,
        {"security_question": "security_question", "security_answer": "security_answer"},
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["security_question"], "security_question")
    snapshot.assert_match(response.data["security_answer"], "security_answer")


@pytest.mark.django_db
def test_get_phone_by_passport(client, register_client, snapshot):
    get_phone_by_passport_url = reverse("phone_by_passport")
    url = f"{get_phone_by_passport_url}?passport_number=0000000029"
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["mobile_phone"], "79311111151")


@pytest.mark.django_db
def test_check_is_client(client, register_client, snapshot):
    phone = register_client.data["client_id"]["mobile_phone"]
    is_client_url = reverse("check_on_client")
    reset_password_url_with_params = f"{is_client_url}?mobile_phone={phone}"
    response = client.get(reset_password_url_with_params)

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.data["client_status"], "NOT_REGISTERED")
    snapshot.assert_match(response.data["mobile_phone"], "79311111151")


@pytest.mark.django_db
def test_reset_pin(client, register_client, snapshot):
    set_pin_url = reverse("pin_code_obtain")
    data = {"client_id": register_client.data["client_id"]["id"], "pin_code": "123456"}
    client.post(set_pin_url, data)

    reset_pin_url = reverse("reset_pin")
    data = {"client_id": register_client.data["client_id"]["id"], "pin_code": "654321"}
    response = client.patch(reset_pin_url, data)
    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(json.dumps(response.json()), "pin_code.json")
