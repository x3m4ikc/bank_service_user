from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from .models import Client, PassportData, PinCode, UserProfile
from .service import sign_up_client, sign_up_not_client


class LogInSerializer(serializers.Serializer):
    Login = serializers.CharField(max_length=200)
    Password = serializers.CharField(max_length=200)


class TokenLogInSerialiser(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField(read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(required=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "uuid",
            "mobile_phone",
            "accession_date",
            "first_name",
            "last_name",
            "middle_name",
            "country_of_residence",
            "client_status",
            "is_staff",
            "is_superuser",
            "is_active",
            "password",
        )
        extra_kwargs = {
            "mobile_phone": {"validators": []},
        }


class PassportSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(required=False)
    nationality = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    passport_number = serializers.CharField(max_length=20)

    class Meta:
        model = PassportData
        fields = (
            "id",
            "passport_number",
            "client_id",
            "nationality",
            "birth_date",
        )
        read_only_fields = ["passport_number"]

    def validate_passport_number(self, value):
        if not value.isdigit() or len(value) > 20:
            raise serializers.ValidationError
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    client_id = ClientSerializer()
    passport_from_client = PassportSerializer(required=False)

    class Meta:
        model = UserProfile
        fields = (
            "id",
            "client_id",
            "security_question",
            "security_answer",
            "email",
            "app_registration_date",
            "passport_from_client",
        )

    @swagger_serializer_method(ClientSerializer)
    def create(self, validated_data):
        user = sign_up_not_client(validated_data)
        return user

    @swagger_serializer_method(ClientSerializer)
    def update(self, instance, validated_data):
        user = sign_up_client(instance, validated_data)
        return user


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("security_question", "security_answer")


class ResetPasswordClient(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"


class MobilePhoneSerializer(serializers.Serializer):
    mobile_phone = serializers.CharField(max_length=11)

    def validate_mobile_phone(self, val):
        if not val.isdigit() or len(val) > 11:
            raise serializers.ValidationError
        return val


class PinCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinCode
        fields = "__all__"

    def validate_pin_code(self, value):
        """pin_code field validation."""
        if not value.isdigit():
            raise serializers.ValidationError("PIN code must contain only digits.")
        return value
