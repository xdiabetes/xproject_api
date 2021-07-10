from django.conf.urls import url
from django.http import HttpResponse
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from xapp.api_v1.views.UserProfileViews import UserProfileRUView, UserProfileAuthTokenView, \
    SendXprojectCode

schema_view = get_schema_view(
    openapi.Info(
        title="CafePay API",
        default_version='development version',
        description="CafePay API Documentation\n@spsina\n@SadafAsad",
        contact=openapi.Contact(email="snparvizi75@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def error500(request):
    a = 1 / 0
    return HttpResponse()


urlpatterns = [

    # user profile
    path('user-profile/',
         UserProfileRUView.as_view(), name="user_profile_ru"),
    path('user-profile/send-code/',
         SendXprojectCode.as_view(), name="user_profile_send_code"),
    path('user-profile/auth-token/',
         UserProfileAuthTokenView.as_view(), name="user_profile_auth_token"),

    path('error500/', error500),

    # docs
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
