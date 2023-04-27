import datetime
import uuid

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        extra_fields.setdefault("accession_date", datetime.datetime.now())
        extra_fields.setdefault("country_of_residence", True)
        extra_fields.setdefault("uuid", uuid.uuid4())

        if not mobile_phone:
            raise ValueError("The mobile phone must be set")
        user = self.model(mobile_phone=mobile_phone, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, mobile_phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("accession_date", datetime.datetime.utcnow())
        extra_fields.setdefault("country_of_residence", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(mobile_phone, password, **extra_fields)
