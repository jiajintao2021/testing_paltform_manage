from django.contrib import admin


# Register your models here.


from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, forms, ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError

from testing_manage.models import CustomUsers


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

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'username', 'name', 'is_superuser', 'is_staff', 'is_active', )
    list_filter = ('is_superuser', 'is_staff', )
    fieldsets = (
        # (None, {'fields': ('email', 'password')}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(CustomUsers, CustomUserAdmin)
admin.site.unregister(Group)
