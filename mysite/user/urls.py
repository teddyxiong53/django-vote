from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.RegisterView.as_view(), name='logout'),
    path('login', views.RegisterView.as_view(), name='login'),
    # path('logout', views.RegisterView.as_view(), name='logout'),
]
