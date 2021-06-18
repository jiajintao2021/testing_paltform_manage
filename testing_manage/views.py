from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy

from django.views import View
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import ListView
from django.views.static import FileResponse

from report_manage.models import ReportTotalModel, TestTypeInfo, ReportErrorTotalModel, TestVersionModel, CarInfoModel
from testing_manage import forms
from testing_manage.forms import FilesAddForm, MonkeyReportForm
from testing_manage.models import FilesModel


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


class MonkeyReportView(ListView):
    template_name = 'testing_platform/monkey_report/monkey_report.html'
    model = ReportTotalModel
    context_object_name = 'monkey_report'
    # queryset = ReportTotalModel.objects.all()

    def get_queryset(self):
        # 获取monkey的ID
        test_type_info = TestTypeInfo.objects.filter(code='monkey').first()
        queryset = self.model.objects.filter(test_type_id=test_type_info.id)
        return queryset


class MonkeyReportColStackChartView(LoginRequiredMixin, SingleObjectMixin, TemplateView):
    template_name = 'testing_platform/monkey_report/monkey_report.html'

    def get_context_data(self, **kwargs):
        test_type_info = TestTypeInfo.objects.filter(code='monkey').first()
        context = super(SingleObjectMixin, self).get_context_data(**kwargs)
        context['monkey_report_1'] = ReportTotalModel.objects.filter(test_type_id=test_type_info.id)
        context['car_info'] = CarInfoModel.objects.filter(is_delete=False)
        context['object'] = self.object
        return context

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.object = MonkeyReportForm(request.GET)
        self.object.is_valid()
        print(self.object.errors)
        print(self.object.cleaned_data)
        return super(MonkeyReportColStackChartView, self).get(request, *args, **kwargs)

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
            print(report_error_obj)
            test_version_obj = TestVersionModel.objects.filter(id=obj.test_version_id).first()
            report_dict[test_version_obj.code] = report_error_obj.to_dict()
        return report_dict
