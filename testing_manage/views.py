from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
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
from testing_manage.forms import FilesAddForm, QueryTestVersionForm, ReportTestVersionsForm
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


class MonkeyReportView(LoginRequiredMixin, SingleObjectMixin, TemplateView):
    template_name = 'testing_platform/monkey_report/monkey_report.html'

    def get(self, request, *args, **kwargs):
        car_name = kwargs.get('car_name')

        get_data = request.GET.copy()
        get_data.setlistdefault(
            'position', DevicePositionModel.objects.filter(cardevicepositionmodel__car__name=car_name))
        get_data.setlistdefault('mode_codes', ModeInfoModel.objects.filter(is_delete=False))
        get_data.setdefault('end_time', now_date())
        get_data.setdefault('start_time', now_date_30())

        self.test_version_query_object = QueryTestVersionForm(car_name=car_name, data=get_data,)
        self.test_version_query_object.is_valid()
        # 在统计的时候不需要查询test version
        if 'test_versions' not in get_data:
            test_versions = TestVersionModel.objects.filter(
                date__gte=get_data.get('start_time'), date__lt=get_data.get('end_time'),
                position_id__in=get_data.getlist('position'), mode_id__in=get_data.getlist('mode_codes'))
        else:
            test_versions = get_data.getlist('test_versions')
            test_versions = TestVersionModel.objects.filter(id__in=test_versions)
        self.test_version_object = ReportTestVersionsForm(
            test_version_queryset=test_versions, data={'test_versions': test_versions})
        self.test_version_object.is_valid()
        return super(MonkeyReportView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        根据测试版本号的个数，判断展示的类型
        """
        context = super(SingleObjectMixin, self).get_context_data(**kwargs)
        context['test_version_query_object'] = self.test_version_query_object
        context['test_version_object'] = self.test_version_object
        test_versions = self.test_version_object.data.get('test_versions')
        context['report_total_1'] = self.report_1(
            ReportErrorTotalModel.objects.filter(report_total__test_version__in=test_versions))
        return context

    def report_1(self, queryset):
        """
        需要展示的内容：
        test_version[x]
        error_number[y]
        content[19errors]
        """
        return {
            obj.report_total.test_version.code: obj.to_dict() for obj in queryset
        }
