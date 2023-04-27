import datetime
import random

import jwt
from django.contrib.auth import logout
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, mixins, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .authentication import ClientJwtAuthentication
from .models import Client, EmailBlockSending, PassportData, PinCode, UserProfile, Verification
from .serializers import (
    ClientSerializer,
    LogInSerializer,
    MobilePhoneSerializer,
    PassportSerializer,
    PinCodeSerializer,
    QuestionSerializer,
    ResetPasswordClient,
    TokenLogInSerialiser,
    UserProfileSerializer,
)
from .service import Service


class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer
    authentication_classes = (ClientJwtAuthentication,)
    service = Service()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = serializer.validated_data
        try:
            client_obj = self.service.checkclient(client)
            if client_obj:
                refresh = RefreshToken.for_user(client_obj)
                serializer = TokenLogInSerialiser(
                    dict(access_token=refresh.access_token, refresh_token=refresh)
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"Клиент с указанными данными не найден"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LogoutAPIView(APIView):
    authentication_classes = (ClientJwtAuthentication,)
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        operation_summary="Logout user",
    )
    def post(self, request: Request) -> Response:
        try:
            refresh_token = request.headers["Authorization"].split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SignUpNotClientView(generics.CreateAPIView):
    authentication_classes = (ClientJwtAuthentication,)
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class SignUpClientView(generics.UpdateAPIView):
    authentication_classes = (ClientJwtAuthentication,)
    http_method_names = ["patch"]
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        client_obj = Client.objects.get(mobile_phone=self.request.data["client_id"]["mobile_phone"])
        user_profile_obj = UserProfile.objects.get(client_id=client_obj)
        return user_profile_obj


class ResetPasswordView(APIView):
    authentication_classes = (ClientJwtAuthentication,)

    @swagger_auto_schema(
        operation_summary="Change password",
        manual_parameters=[
            openapi.Parameter(
                name="New password",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                required=True,
            )
        ],
        request_body=openapi.Schema(type=openapi.TYPE_INTEGER, name="Mobile phone"),
    )
    def patch(self, request):
        mobile_phone = request.GET.get("mobile_phone")
        try:
            client_obj = Client.objects.get(mobile_phone=mobile_phone)
            client = ResetPasswordClient(
                instance=client_obj,
                data={"password": request.data.get("new_password")},
                partial=True,
            )
            client.is_valid(raise_exception=True)
            client.save()
            return Response({"client": client.data}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AuthenticationView(generics.GenericAPIView):
    authentication_classes = (ClientJwtAuthentication,)
    serializer_class = TokenLogInSerialiser
    authentication = ClientJwtAuthentication()

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = self.authentication.get_validated_token(
                serializer.validated_data["access_token"]
            )
            user_obj = self.authentication.get_user(token)
            serializer = ClientSerializer(user_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PhoneByPassportView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    authentication_classes = (ClientJwtAuthentication,)

    def get_object(self):
        passport_serializer = PassportSerializer(data=self.request.GET)
        passport_serializer.is_valid(raise_exception=True)
        passport_data = passport_serializer.validated_data

        passport = PassportData.objects.get(passport_number=passport_data.get("passport_number"))
        client = Client.objects.get(id=passport.client_id.id)
        return client


class EmailVerify(mixins.UpdateModelMixin, GenericAPIView):
    authentication_classes = (ClientJwtAuthentication,)
    service = Service()

    # TODO: Получение запроса из другого сервиса (ожидает готовности сервиса)

    def get_user(self, mobile_phone):
        client_obj = Client.objects.get(mobile_phone=mobile_phone)
        user_profile_obj = UserProfile.objects.get(client_id=client_obj)
        return user_profile_obj

    def put(self, request):
        try:
            token = request.headers["Authorization"]
            mobile_phone = jwt.decode(token, options={"verify_signature": False})["mobile_phone"]
        except BaseException:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_profile_obj = self.get_user(mobile_phone)
        email = user_profile_obj.email
        data = {"email": email}

        sms_block_expiration = datetime.timedelta(seconds=30)
        try:
            EmailBlockSending.objects.create(
                email=user_profile_obj, sending_count=1, sms_block_expiration=sms_block_expiration
            )
            verification_code = random.randint(100000, 999999)
            code_expiration = datetime.timedelta(minutes=15)
            Verification.objects.create(
                email=user_profile_obj,
                verification_code=verification_code,
                code_expiration=code_expiration,
            )

        except BaseException:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        data["verification_code"] = verification_code

        self.service.send_code_via_email(email, verification_code)
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            token = request.headers["Authorization"]
        except KeyError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            mobile_phone = jwt.decode(token, options={"verify_signature": False})["mobile_phone"]
            user_profile_obj = self.get_user(mobile_phone)
            email = user_profile_obj.email
            data = {"email": email}

            email_block_sending_obj = EmailBlockSending.objects.get(email=user_profile_obj)
            verification_obj = Verification.objects.get(email=user_profile_obj)

        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        delta_time = now - email_block_sending_obj.creation_time_email

        if not delta_time >= email_block_sending_obj.sms_block_expiration:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        verification_code = random.randint(100000, 999999)
        creation_time_code = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
        verification_obj.verification_code = verification_code
        verification_obj.creation_time_code = creation_time_code
        verification_obj.save()
        data["verification_code"] = verification_code

        email_block_sending_obj.sending_count += 1
        time_block = email_block_sending_obj.sms_block_expiration * 2
        email_block_sending_obj.sms_block_expiration = time_block
        email_block_sending_obj.creation_time_email = datetime.datetime.now().replace(
            tzinfo=datetime.timezone.utc
        )
        email_block_sending_obj.save()

        self.service.send_code_via_email(email, verification_code)
        return Response(data, status=status.HTTP_200_OK)


class ResetSecurityQuestion(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (ClientJwtAuthentication,)
    service = Service()

    def get_object(self):
        user = self.request.user
        return user


class IsClientView(generics.RetrieveAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = (ClientJwtAuthentication,)

    @swagger_auto_schema(
        responses={
            status.HTTP_409_CONFLICT: "user is client and registered",
            status.HTTP_200_OK: "User is not registered or is not client",
        },
        operation_summary="Check registration",
        manual_parameters=[
            openapi.Parameter(
                name="phone_number",
                in_=openapi.IN_QUERY,  # is url`a
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            client = self.get_object()
            if self.get_serializer(client).data.get("client_status") != "NOT_REGISTERED":
                raise ValueError
            return Response(
                {"mobile_phone": client.mobile_phone, "client_status": client.client_status},
                status=status.HTTP_200_OK,
            )
        except ObjectDoesNotExist:
            return Response(
                {"mobile_phone": request.GET["mobile_phone"], "client_status": "NOT_CLIENT"},
                status=status.HTTP_200_OK,
            )
        except ValueError:
            return Response(
                {"mobile_phone": request.GET["mobile_phone"], "client_status": "REGISTERED"},
                status=status.HTTP_409_CONFLICT,
            )

    def get_object(self):
        mobile_serializer = MobilePhoneSerializer(data=self.request.GET)
        mobile_serializer.is_valid(raise_exception=True)
        mobile_phone = mobile_serializer.data["mobile_phone"]
        client = Client.objects.get(mobile_phone=mobile_phone)
        return client


class PinCodeObtainView(generics.CreateAPIView):
    """
    Custom view for creating a user PIN-code.
    """

    authentication_classes = (ClientJwtAuthentication,)
    serializer_class = PinCodeSerializer
    queryset = PinCode.objects.all()


class ResetPinCode(generics.UpdateAPIView):
    authentication_classes = (ClientJwtAuthentication,)
    serializer_class = PinCodeSerializer
    queryset = PinCode.objects.all()

    def get_object(self):
        pin_code_queryset = self.get_queryset()
        obj = pin_code_queryset.get(client_id=self.request.data["client_id"])
        return obj
