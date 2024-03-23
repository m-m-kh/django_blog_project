from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import CustomUser
from .google import google_auth
from django.core.exceptions import RequestAborted
from django.conf import settings

class SignUp(View):
    template_name = 'accounts/signup.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(SignUp, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        auth = google_auth.GoogleAuth(request)
        auth_url = auth.generate_login_url()
        request.session['auth_url'] = auth_url

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        auth_url = request.session.get('auth_url')
        return redirect(auth_url[0])


class SignUpConfirm(View):

    def dispatch(self, request, *args, **kwargs):
        if auth_url:=request.session.get('auth_url'):
            if auth_url[1] != request.GET.get('state'):
                messages.warning(request, 'try again')
                return redirect('signup')
        else:
            messages.warning(request, 'try again')
            return redirect('signup')
        return super(SignUpConfirm, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        auth = google_auth.GoogleAuth(request)
        auth_user = auth.get_user_info(url=request.build_absolute_uri().replace('http://', 'https://'))
        del request.session['auth_url']
        # {'id': '108214459709151642195', 'email': 'khademim092092@gmail.com', 'verified_email': True,
        #  'name': 'Djrj Jfjr', 'given_name': 'Djrj',
        #  'family_name': 'Jfjr',
        #  'picture': 'https://lh3.googleusercontent.com/a/ACg8ocIG9IXH1Z-PenJWL-YntQ0FCMqwKEjy8jPZwBtYfwWt=s96-c',
        #  'locale': 'fa'}
        user = get_user_model().objects.get_or_create(email=auth_user['email'],
                                             username=auth_user['email'].split('@')[0],
                                             profile_id=auth_user['id'])

        login(request, user=user[0])

        return redirect(settings.LOGIN_REDIRECT_URL)

class LogOut(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise RequestAborted
        return super(LogOut, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_REDIRECT_URL)