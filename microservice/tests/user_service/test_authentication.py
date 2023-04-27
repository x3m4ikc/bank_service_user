import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_authentication(login, client, snapshot):
    authentication = reverse("authentication")
    response = client.post(authentication, login)
    snapshot.assert_match(response.data["mobile_phone"], "9311111151")
    assert response.status_code == 200
