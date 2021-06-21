import datetime

from django import forms
from django.contrib.auth.forms import UsernameField

from django.contrib.auth.views import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from report_manage.models import CarInfoModel, ReportTotalModel, TestVersionModel, ModeInfoModel, DevicePositionModel
from testing_manage.models import FilesModel
from testing_manage.utils import now_date, now_date_30


class LoginForm(AuthenticationForm):
    # username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    username = UsernameField(
        label=_('用户账号'),
        widget=forms.TextInput(attrs={'placeholder': 'xxxxx@email.com | username'}))
    password = forms.CharField(
        label=_("密码"),
        strip=False,
        # widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
        widget=forms.PasswordInput(),
    )

    error_messages = {
        'invalid_login': _(
            "用户名和密码错误，请输入正确的用户名和密码！"
        ),
        'inactive': _("该账号异常，联系管理人员！"),
    }

    def clean_username(self):
        username = self.cleaned_data.get('username', None)
        if not username:
            raise ValidationError(message=self.error_messages['invalid_login'])
        return username


class FilesAddForm(forms.ModelForm):

    class Meta:
        model = FilesModel
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']
        if FilesModel.objects.filter(name=name):
            raise ValidationError('该名称已经存在！')
        return name


class MonkeyReportME5Form(forms.Form):
    start_time = forms.DateField(label='时间范围', required=False, initial=now_date_30)
    end_time = forms.DateTimeField(label='结束时间', required=False, initial=now_date)
    test_versions = forms.ModelMultipleChoiceField(
        label='测试版本号',
        queryset=None,
        required=False,
        widget=forms.CheckboxSelectMultiple)
    position = forms.ModelMultipleChoiceField(
        label='设备位置',
        queryset=DevicePositionModel.objects.filter(is_delete=False, cardevicepositionmodel__car__name='ME5'),
        widget=forms.CheckboxSelectMultiple)
    mode_codes = forms.ModelMultipleChoiceField(
        label='编译模式',
        queryset=ModeInfoModel.objects.filter(is_delete=False),
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, test_versions_queryset=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['test_versions'].queryset = test_versions_queryset


class MonkeyReportForm(forms.Form):
    # test_version =
    start_time = forms.DateField(label='时间范围', required=False, initial=now_date_30)
    end_time = forms.DateTimeField(label='结束时间', required=False, initial=now_date)
    # car_codes = forms.ModelChoiceField(
    #     queryset=CarInfoModel.objects.filter(is_delete=False),
    #     label='汽车名称',
    #     widget=forms.RadioSelect)
    test_versions = forms.ModelMultipleChoiceField(
        label='测试版本号',
        queryset=TestVersionModel.objects.filter(is_delete=False),
        widget=forms.CheckboxSelectMultiple)
    mode_codes = forms.ModelMultipleChoiceField(
        label='编译模式',
        queryset=ModeInfoModel.objects.filter(is_delete=False),
        widget=forms.CheckboxSelectMultiple)
    position = forms.ModelMultipleChoiceField(
        label='设备位置',
        queryset=DevicePositionModel.objects.filter(is_delete=False),
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = ReportTotalModel
        fields = '__all__'

    def clean_car_codes(self):
        car_codes = self.cleaned_data.get('car_codes')
        return car_codes

    def clean_end_time(self):
        date = self.cleaned_data.get('end_time')
        if not date:
            date = now_date()
        return date

    def clean_start_time(self):
        date = self.cleaned_data.get('start_time')
        if not date:
            date = now_date_30()
        return date
