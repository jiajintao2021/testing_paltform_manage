from django.urls import path

from testing_manage.views import Index, CustomLoginView

urlpatterns = [
    path('index/', Index.as_view(), name='index'),

    path('login/', CustomLoginView.as_view(), name='login'),
]
