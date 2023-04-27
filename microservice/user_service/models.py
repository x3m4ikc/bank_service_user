from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models

from .authentication import ClientJwtAuthentication
from .user_manager import CustomUserManager


class Client(AbstractBaseUser, PermissionsMixin):
    """Client Model"""

    CLIENT_STATUS_CHOICE = (
        ("ACTIVE", "ACTIVE"),
        ("NOT_ACTIVE", "NOT_ACTIVE"),
        ("NOT_REGISTERED", "NOT_REGISTERED"),
    )
    uuid = models.UUIDField(null=False, unique=True)
    first_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    middle_name = models.CharField(max_length=30)
    accession_date = models.DateTimeField(null=False)
    country_of_residence = models.BooleanField(null=False)
    client_status = models.CharField(
        max_length=20, choices=CLIENT_STATUS_CHOICE, default="NOT_REGISTERED"
    )
    mobile_phone = models.CharField(max_length=11, null=False, unique=True)
    password = models.CharField(max_length=200, null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "mobile_phone"
    is_authenticated = ClientJwtAuthentication

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def __str__(self):
        return self.mobile_phone


class PassportData(models.Model):
    """PassportData Model"""

    passport_number = models.CharField(max_length=20, unique=True, null=False)
    client_id = models.OneToOneField(
        Client, related_name="passport_from_client", on_delete=models.CASCADE
    )
    issuance_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(auto_now_add=True)
    nationality = models.CharField(max_length=50)
    birth_date = models.DateTimeField()


class Fingerprint(models.Model):
    """Fingerprint Model"""

    fingerprint = models.CharField(max_length=32, unique=True, null=False)
    client_id = models.ForeignKey(Client, on_delete=models.CASCADE)


class UserProfile(models.Model):
    """User profile model"""

    client_id = models.OneToOneField(
        Client, related_name="profile_from_client", on_delete=models.CASCADE
    )
    sms_notification = models.BooleanField(default=True)
    push_notification = models.BooleanField(default=True)
    email = models.CharField(max_length=50, null=True)
    security_question = models.CharField(max_length=50, null=False)
    security_answer = models.CharField(max_length=50, null=False)
    app_registration_date = models.DateField(auto_now_add=True)
    email_subscription = models.BooleanField(default=False)


class EmailBlockSending(models.Model):

    sending_count = models.IntegerField(default=0)
    creation_time_email = models.DateTimeField(auto_now_add=True)
    sms_block_expiration = models.DurationField()
    email = models.OneToOneField(UserProfile, related_name="email_block", on_delete=models.CASCADE)


class Verification(models.Model):

    verification_code = models.IntegerField()
    creation_time_code = models.DateTimeField(auto_now_add=True)
    code_expiration = models.DurationField()
    email = models.OneToOneField(UserProfile, related_name="email_verify", on_delete=models.CASCADE)


class PinCode(models.Model):
    """PIN-code model."""

    client_id = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Client ID",
        help_text="Please enter client ID",
    )
    pin_code = models.CharField(
        max_length=6,
        verbose_name="User PIN code",
        help_text='Please enter 6-digit PIN code according to the format: "123456"',
        validators=[MinLengthValidator(6)],
    )
