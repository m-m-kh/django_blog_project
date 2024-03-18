from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
class SignUp(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
