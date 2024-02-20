from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import requests
from django.shortcuts import redirect
from django.urls import reverse
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client



class CustomEmailConfirmView(APIView):
    permission_classes = [AllowAny, ]
    def get(self, request, key):
        frontend_origin = settings.FRONTEND_ORIGIN
        verify_email_url = settings.CUSTOM_VERIFY_EMAIL_LINK
        response = requests.post(verify_email_url, {'key': key})
        if response.status_code == 200:
            login_url = f"{frontend_origin}/login"  # Vue.jsのログインページのURL
            print(login_url)
            return redirect(login_url)
        else:
            signup_url = f"{frontend_origin}/signup"  # Vue.jsのログインページのURL
            return redirect(signup_url)


class GoogleLogin(SocialLoginView): # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'http://127.0.0.1:8000/api/posts/'
    client_class = OAuth2Client