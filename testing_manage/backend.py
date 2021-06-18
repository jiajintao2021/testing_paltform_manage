"""
@TIME: 2021/6/3 18:21
@AUTHOR: JiaJinTao
"""
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from ldap3 import Server, Connection
from ldap3.core.exceptions import LDAPBindError

from testing_manage.models import CustomUsers
from testing_manage_platform.settings import LDAP_HOST, LDAP_PORT, LDAP_ADDRESS


class CustomBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None or password is None:
            return

        if request.path == '/admin/login/':
            if '@' not in username:
                return
            try:
                user = CustomUsers.objects.get(email=username)
            except CustomUsers.DoesNotExist:
                return None
            if user.check_password(password) and user.is_active and user.is_staff:
                return user
            return

        email = username
        if '@' not in email:
            email = username + '@enovatemotors.com'
        server = Server(host=LDAP_ADDRESS)
        try:
            conn = Connection(server, user=email, password=password, auto_bind=True)
        except LDAPBindError:
            return None

        user = None
        if conn:
            try:
                user = CustomUsers.objects.get(username=username, email=email)
            except CustomUsers.DoesNotExist:
                user = CustomUsers(email=email, username=username)
                user.set_password('123456')
                user.is_staff = False
                user.is_active = True
                user.is_superuser = False
                user.save()
        conn.unbind()
        return user

    def get_user(self, user_id):
        try:
            return CustomUsers.objects.get(pk=user_id)
        except CustomUsers.DoesNotExist:
            return None
