from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'goods'

urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),

    # path('', views.IndexView.as_view(), name='index'),
]
