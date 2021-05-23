from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView

from testing_manage import forms


class CustomLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'


class Index(TemplateView):
    template_name = 'base.html'
