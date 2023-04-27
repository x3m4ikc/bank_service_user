import enum
import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import transaction

from .models import Client, PassportData, UserProfile


class Service:
    def checkclient(self, data, *args, **kwargs):
        password = data["Password"]
        login = data["Login"]
        try:
            client_obj = Client.objects.get(mobile_phone=login)
            if password == client_obj.password:
                return client_obj
            else:
                raise ObjectDoesNotExist
        except ObjectDoesNotExist:
            client_obj = PassportData.objects.get(passport_number=login)
            if password == client_obj.password:
                return client_obj
            else:
                raise Exception
        except Exception:
            logger = logging.getLogger("main")
            logger.error("Некорректный пароль")
            raise ValueError("Некорректный пароль")

    def send_code_via_email(self, email, verification_code):
        subject = "Verifying your account"
        message = f"Your verification code {verification_code}"
        send_mail(subject, message, "settings.EMAIL_HOST_USER", [email])


class ClientStatus(str, enum.Enum):
    NOT_ACTIVE = "NOT_ACTIVE"


def sign_up_not_client(validated_data):
    client_profile_data = validated_data.pop("client_id")
    client_profile_data["uuid"] = uuid.uuid4()
    passport_data = validated_data.pop("passport_from_client")

    with transaction.atomic():
        client = Client.objects.create(**client_profile_data)
        client.set_password(client_profile_data["password"])
        user_profile = UserProfile.objects.create(**validated_data, client_id=client)
        PassportData.objects.create(**passport_data, client_id=client)
    return user_profile


def sign_up_client(instance, validated_data):
    client_data = validated_data.pop("client_id")
    validated_data.pop("passport_from_client")

    client = instance.client_id
    client.client_status = ClientStatus.NOT_ACTIVE
    for attr, value in client_data.items():
        setattr(client, attr, value)
    client.save()

    for attr, value in validated_data.items():
        setattr(instance, attr, value)
    instance.save()

    return instance
