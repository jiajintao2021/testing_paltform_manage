"""
@TIME: 2021/6/3 15:34
@AUTHOR: JiaJinTao
"""
from django.middleware.common import CommonMiddleware
from ldap3 import Server, Connection

from testing_manage_platform.settings import LDAP_HOST, LDAP_PORT


class CustomMiddleware(CommonMiddleware):
    intercept_list = [('login', 'POST', )]

    def process_request(self, request):
        ldap_server = Server(host=LDAP_HOST, port=LDAP_PORT)
        print(request.path, request.method)
        for key_word, method in self.intercept_list:
            if key_word in request.path and request.method == method:
                username = request.POST.get('username')

        return super(CustomMiddleware, self).process_request(request)

    def process_response(self, request, response):
        return super(CustomMiddleware, self).process_response(request, response)
