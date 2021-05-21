from django.shortcuts import render

# Create your views here.


from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):

    pass


class Index(TemplateView):
    template_name = 'base.html'
