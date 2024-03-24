import pathlib

import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.conf import settings
from django.urls import reverse

SCOPES = ['openid',
          "https://www.googleapis.com/auth/userinfo.profile",
          'https://www.googleapis.com/auth/userinfo.email']

ROOT_DIR = pathlib.Path(__file__).parent

# REDIRECT_URI = get_current_site() + reverse(settings.GOOGLE_AUTH_REDIRECT_URL)


class GoogleAuth:
    def __init__(self, request):
        self.flow = InstalledAppFlow.from_client_secrets_file(
        ROOT_DIR.joinpath("client_secret.json"), SCOPES,
                )

        if settings.DEBUG:
            self.flow.redirect_uri = 'http://localhost:8000' + reverse(settings.GOOGLE_AUTH_CALLBACK_URL)
        else:
            self.flow.redirect_uri = request.get_host() + reverse(settings.GOOGLE_AUTH_CALLBACK_URL)
    def generate_login_url(self):
        return self.flow.authorization_url()
        
        
    def __get_cred(self, url):
        self.flow.fetch_token(authorization_response=url)
        return self.flow.credentials

    def get_user_info(self, url):
        cred = self.__get_cred(url)
        service = build("oauth2", "v2", credentials=cred)
        profile_info = service.userinfo().get().execute()
        return profile_info
        
