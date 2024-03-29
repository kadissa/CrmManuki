from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login')
]
