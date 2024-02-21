from django.urls import path, re_path
from dj_rest_auth.app_settings import api_settings

from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView,
    PasswordResetView, UserDetailsView,
)
from dj_rest_auth.registration.views import (
    RegisterView, VerifyEmailView, ResendEmailVerificationView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CustomEmailConfirmView, GoogleLogin
from allauth.socialaccount.providers.oauth2.views import (OAuth2LoginView, OAuth2CallbackView)
from django.views.generic import TemplateView


urlpatterns = [
    # URLs that do not require a session or valid token
    path('signup/', RegisterView.as_view(), name='rest_register'),
    path('google/', GoogleLogin.as_view(), name='google_login'),
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    re_path(r'account-confirm-email/(?P<key>[-:\w]+)/$', CustomEmailConfirmView.as_view(),name='account_confirm_email',),
    path("account_email_verification_sent", TemplateView.as_view(), name="account_email_verification_sent"),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/',  PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
]

if api_settings.USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ]