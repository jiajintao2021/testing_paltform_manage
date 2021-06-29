"""
@TIME: 2021/6/23 11:34
@AUTHOR: JiaJinTao
"""
from django import forms

from report_manage.models import ErrorLevelModel, ErrorInfoModel, ErrorNameLevelModel


class ErrorLevelForm(forms.ModelForm):
    class Meta:
        model = ErrorLevelModel
        fields = '__all__'


class ErrorInfoForm(forms.ModelForm):
    class Meta:
        model = ErrorInfoModel
        fields = '__all__'


class ErrorNameLevelForm(forms.ModelForm):
    class Meta:
        model = ErrorNameLevelModel
        fields = '__all__'
