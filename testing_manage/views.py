from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.static import FileResponse

from report_manage.models import ReportTotalModel, TestTypeInfo, ReportErrorTotalModel, TestVersionModel, CarInfoModel, \
    CarDevicePositionModel, ModeInfoModel, DevicePositionModel
from testing_manage import forms
from testing_manage.forms import FilesAddForm, MonkeyReportForm, MonkeyReportME5Form
from testing_manage.models import FilesModel
from testing_manage.utils import now_date_30, now_date


class CustomLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'


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


class MonkeyReportME5View(LoginRequiredMixin, SingleObjectMixin, TemplateView):
    template_name = 'testing_platform/monkey_report/monkey_report.html'

    def get_context_data(self, **kwargs):
        test_type_info = TestTypeInfo.objects.filter(code='monkey').first()
        context = super(SingleObjectMixin, self).get_context_data(**kwargs)
        context['monkey_report_1'] = ReportTotalModel.objects.filter(test_type_id=test_type_info.id)
        context['object'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        content = {}
        car_name = 'ME5'
        print(request.GET, kwargs)
        position = request.GET.get('position')
        if position:
            content['position'] = position
        else:
            content['position'] = DevicePositionModel.objects.filter(
                is_delete=False,
                cardevicepositionmodel__car__name=car_name)

        start_time = request.GET.get('start_time', now_date_30())
        if start_time:
            content['start_time'] = start_time
        end_time = request.GET.get('end_time', now_date())
        if end_time:
            content['end_time'] = end_time
        #
        mode_codes = request.GET.get('mode_codes')
        if mode_codes:
            content['modes'] = mode_codes
        else:
            content['modes'] = ModeInfoModel.objects.all()

        test_versions = request.GET.get('test_versions')
        if test_versions:
            content['test_versions'] = test_versions
        else:
            content['test_versions'] = TestVersionModel.objects.filter(
                is_delete=False, date__lte=content['end_time'], date__gte=content['start_time'],
                mode__in=content['modes'], position__in=content['position']
            )

        self.object = MonkeyReportME5Form(
            data={
                'position': content['position'], 'mode_codes': content['modes'],
                'test_versions': content['test_versions']},
            test_versions_queryset=TestVersionModel.objects.filter(
                is_delete=False, date__lte=content['end_time'], date__gte=content['start_time'],
                mode__in=content['modes'], position__in=content['position']
            ),
            initial={
                # 'test_versions': content['test_versions'],
                'start_time': start_time, 'end_time': end_time,
                'mode_codes': content['modes'],
            })
        self.object.is_valid()
        print(self.object.errors)
        print(self.object.cleaned_data)
        return super(MonkeyReportME5View, self).get(request, *args, **kwargs)

    def get_test_version(self):
        pass

    def form_query(self):
        """
        查询表单
        """
        return

    def report_1(self, queryset):
        report_dict = {}
        for obj in queryset:
            report_error_obj = ReportErrorTotalModel.objects.filter(report_total_id=obj.id).first()
            test_version_obj = TestVersionModel.objects.filter(id=obj.test_version_id).first()
            report_dict[test_version_obj.code] = report_error_obj.to_dict()
        return report_dict
