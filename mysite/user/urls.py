from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('login', views.LoginView.as_view(), name='login'),
    path('user', views.RegisterView.as_view(), name='user'),
    path('cart', views.RegisterView.as_view(), name='cart'),
    path('order', views.RegisterView.as_view(), name='order'),
]
