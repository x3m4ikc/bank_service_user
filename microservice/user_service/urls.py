from django.urls import path

from .views import (
    AuthenticationView,
    EmailVerify,
    IsClientView,
    LogInView,
    LogoutAPIView,
    PhoneByPassportView,
    PinCodeObtainView,
    ResetPasswordView,
    ResetPinCode,
    ResetSecurityQuestion,
    SignUpClientView,
    SignUpNotClientView,
)

urlpatterns = [
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("registration", IsClientView.as_view(), name="check_on_client"),
    path("registration/new/", SignUpNotClientView.as_view(), name="sign_up_not_client"),
    path("registration/", SignUpClientView.as_view(), name="sign_up_client"),
    path("login/password", ResetPasswordView.as_view(), name="reset_password"),
    path("security/session/", PhoneByPassportView.as_view(), name="phone_by_passport"),
    path("login/", LogInView.as_view(), name="login"),
    path("authentication/", AuthenticationView.as_view(), name="authentication"),
    path("security/session", EmailVerify.as_view(), name="email_verify"),
    path(
        "user/settings/controls/", ResetSecurityQuestion.as_view(), name="reset_security_question"
    ),
    path("login/pin/", PinCodeObtainView.as_view(), name="pin_code_obtain"),
    path("login/pin/reset/", ResetPinCode.as_view(), name="reset_pin"),
]
