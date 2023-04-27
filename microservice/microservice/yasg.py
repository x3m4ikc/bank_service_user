from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from user_service.authentication import ClientJwtAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Microservice A-GELD",
        default_version="v1",
        description="Endpoints to user_service",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[ClientJwtAuthentication],
)

urlpatterns = [
    re_path(r"swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
