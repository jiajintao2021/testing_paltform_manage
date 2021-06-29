from django.contrib import admin


# Register your models here.


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, forms, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from report_manage.forms import ErrorLevelForm, ErrorInfoForm, ErrorNameLevelForm
from report_manage.models import ErrorLevelModel, ErrorInfoModel, ErrorNameLevelModel
from testing_manage.models import CustomUsers, FilesModel
from testing_manage.forms import FilesAddForm


class CustomUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='登录密码', widget=forms.PasswordInput())
    password2 = forms.CharField(label='重复密码', widget=forms.PasswordInput())

    class Meta:
        model = CustomUsers
        fields = ['email', 'username', ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        print('p1', password1, 'p2', password2)
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='密码')

    class Meta:
        model = CustomUsers
        fields = '__all__'


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = CustomUserUpdateForm
    add_form = CustomUserCreateForm

    list_display = ('email', 'username', 'name', 'is_superuser', 'is_staff', 'is_active', )
    list_filter = ('is_superuser', 'is_staff', )
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class FilesAdmin(admin.ModelAdmin):
    form = FilesAddForm
    fieldsets = [
        (None, {'fields': ['name', 'file', 'desc', 'is_delete']})
    ]
    list_display = ['name', 'file', 'is_delete', 'desc', ]
    list_filter = ['is_delete', ]
    search_fields = ['name', ]


class ErrorLevelAdmin(admin.ModelAdmin):
    form = ErrorLevelForm
    fieldsets = [
        (None, {'fields': ['level', 'is_delete']})
    ]
    list_display = ['level', 'is_delete']
    list_filter = ['is_delete', 'level']
    search_fields = ['level']


class ErrorInfoAdmin(admin.ModelAdmin):
    form = ErrorInfoForm
    fieldsets = [
        (None, {'fields': ['error_name', 'is_delete']})
    ]
    list_display = ['error_name', 'is_delete']
    list_filter = ['is_delete']
    search_fields = ['error_name']


class ErrorNameLevelAdmin(admin.ModelAdmin):
    form = ErrorNameLevelForm
    fieldsets = [
        (None, {'fields': ['error_name', 'level', 'is_delete']})
    ]
    list_display = ['error_name', 'level', 'is_delete']
    list_filter = ['is_delete', 'level']
    search_fields = ['error_name', 'level']


admin.site.register(CustomUsers, CustomUserAdmin)
admin.site.register(FilesModel, FilesAdmin)
admin.site.register(ErrorLevelModel, ErrorLevelAdmin)
admin.site.register(ErrorInfoModel, ErrorInfoAdmin)
admin.site.register(ErrorNameLevelModel, ErrorNameLevelAdmin)

admin.site.unregister(Group)
