from django.conf.urls import url
from django.urls import include, path
from .views import inicio, waiters
from apps.Pikada.views import inicio, waiters

app_name='pikadaapp'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('waiters', waiters, name='waiters'),
]