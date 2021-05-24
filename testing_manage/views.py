from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView

from testing_manage import forms
from testing_manage.models import FilesModel


class CustomLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'


class Index(TemplateView):
    template_name = 'testing_platform/index.html'


class FilesList(ListView):
    template_name = 'testing_platform/files/files_list.html'
    model = FilesModel
    queryset = FilesModel.objects.filter(is_delete=False)
    context_object_name = 'file_list'
