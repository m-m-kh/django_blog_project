import requests
from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, UserChangeForm
from .models import CustomUser, EmailConfirmation
from .google import google_auth
from django.core.exceptions import RequestAborted, PermissionDenied
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from random import randint
from django.contrib.auth.tokens import default_token_generator


class SignUp(View):
    template_name = 'accounts/signup.html'
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(SignUp, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        context = {'form' : form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            form = form.save(commit=False)
            form.username = cleaned_data.get('email').split('@')[0]
            form.save()
            token = default_token_generator.make_token(user=form)
            email_confirmation = EmailConfirmation()
            email_confirmation.user = form
            email_confirmation.code = randint(100000,999999)
            email_confirmation.save()

            return redirect('confirm_email', uuid=email_confirmation.pk, token=token)
        context = {'form': form}

        return render(request, self.template_name, context=context)

class ConfirmEmail(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('w')

class GoogleSignUpConfirm(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == "GET":
            if auth_url:=request.session.get('auth_url'):
                if auth_url[1] != request.GET.get('state'):
                    messages.warning(request, 'try again')
                    return redirect('signup')
            else:
                messages.warning(request, 'try again')
                return redirect('signup')
        return super(GoogleSignUpConfirm, self).dispatch(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        auth = google_auth.GoogleAuth(request)
        auth_user = auth.get_user_info(url=request.build_absolute_uri().replace('http://', 'https://'))
        # {'id': '108214459709151642195', 'email': 'khademim092092@gmail.com', 'verified_email': True,
        #  'name': 'Djrj Jfjr', 'given_name': 'Djrj',
        #  'family_name': 'Jfjr',
        #  'picture': 'https://lh3.googleusercontent.com/a/ACg8ocIG9IXH1Z-PenJWL-YntQ0FCMqwKEjy8jPZwBtYfwWt=s96-c',
        #  'locale': 'fa'}
        email = auth_user['email']
        username = auth_user['email'].split('@')[0]
        profile_id = auth_user['id']
        # password = 'wai'+email+'wai'+profile_id


        if not (user := get_user_model().objects.filter(email=email, username=username)):
            user = get_user_model().objects.create(email=email, username=username)
        else:
            user = user[0]

        if not user.password:
            request.session['user_id'] = user.pk
            return redirect('google_set_pass')

        if user.profile_id == '0':
            user.profile_id = profile_id
            user.save()

        login(request, user=user)
        del request.session['auth_url']

        return redirect(settings.LOGIN_REDIRECT_URL)

    def post(self, request, *args, **kwargs):
        if request.session.get('user_id'):
            return redirect('google_set_pass')
        auth = google_auth.GoogleAuth(request)
        auth_url = auth.generate_login_url()
        request.session['auth_url'] = auth_url
        return redirect(auth_url[0])

class GoogleSetPass(View):

    # def dispatch(self, request, *args, **kwargs):
    #     if not request.session.get('user_id'):
    #         raise PermissionDenied
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=request.session['user_id'])
        form = SetPasswordForm(user)
        context = {'form': form}
        return render(request, 'accounts/set_pass.html', context=context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), pk=request.session['user_id'])
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            del request.session['user_id']
            del request.session['auth_url']
            return redirect(settings.LOGIN_REDIRECT_URL)

        context = {'form': form}
        return render(request, 'accounts/set_pass.html', context=context)

class LogIn(View):
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {'form': form}
        return render(request, 'accounts/login.html', context=context)
    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            login(request, user=form.get_user())
            return redirect(settings.LOGIN_REDIRECT_URL)
        context = {'form': form}

        return render(request, 'accounts/login.html', context=context)

class LogOut(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise RequestAborted
        return super(LogOut, self).dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_REDIRECT_URL)

# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes,force_str
# from django.contrib.auth.tokens import default_token_generator
# class Test(View):
#     def get(self, request):
#         user = get_user_model().objects.last()
#         'c4hxh2-4b46a9446b89633259188ce10bf26074'
#         'c4hxgy-a156dfe1096e668b3bd4687fc4190580'
#         'c4hxgw-e832df422fd6af51aea6376562da898e'
#         print(default_token_generator.check_token(user,'c4hxgw-e832df422fd6awf51aea6376562da898e'))
#         return HttpResponse('w')
