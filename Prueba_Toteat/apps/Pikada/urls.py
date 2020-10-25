from django.conf.urls import url
from django.urls import include, path
from .views import inicio, waiters
from apps.Pikada.views import inicio, waiters, categories, cashiers

app_name='pikadaapp'

urlpatterns = [
    path('', inicio, name='inicio'),
    path('categories', categories, name='categories'),
    path('waiters', waiters, name='waiters'),
    path('cashiers', cashiers, name='cashiers'),
]