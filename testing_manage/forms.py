import datetime

from django import forms
from django.contrib.auth.forms import UsernameField

from django.contrib.auth.views import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from report_manage.models import CarInfoModel, ReportTotalModel
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


class MonkeyReportForm(forms.Form):
    # test_version =
    start_time = forms.DateField(label='开始时间', required=False, initial=now_date_30)
    end_time = forms.DateTimeField(label='结束时间', required=False, initial=now_date)
    car_codes = forms.CharField(
        label='汽车类型', required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox'}))

    class Meta:
        model = ReportTotalModel
        fields = '__all__'

    def clean_car_codes(self):
        car_codes = self.cleaned_data.get('car_codes')
        print(car_codes)
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
