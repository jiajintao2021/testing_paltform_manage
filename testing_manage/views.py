from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.list import ListView
from django.views.static import FileResponse

from testing_manage import forms
from testing_manage.forms import FilesAddForm
from testing_manage.models import FilesModel


class CustomLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'

    def post(self, request, *args, **kwargs):
        return super(CustomLoginView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        return super(CustomLoginView, self).form_valid(form)

    def get_form(self, form_class=None):
        return super(CustomLoginView, self).get_form(form_class)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'testing_platform/index.html'


class DownFile(View):

    def get(self, request, *args, **kwargs):
        file = FilesModel.objects.filter(**kwargs).first()
        response = FileResponse(open(file.file.path, 'rb'),
                                filename=file.file.name,
                                as_attachment=True)
        return response


class FilesListView(LoginRequiredMixin, ListView):
    template_name = 'testing_platform/files/files_list.html'
    model = FilesModel
    queryset = FilesModel.objects.filter(is_delete=False)
    context_object_name = 'file_list'


class FilesAddView(LoginRequiredMixin, CreateView):
    form_class = FilesAddForm
    model = FilesModel
    template_name = 'testing_platform/files/files_add.html'
    initial = {'is_delete': False}
    success_url = reverse_lazy('files-list')
