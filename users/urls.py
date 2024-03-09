from django.urls import path
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutView.as_view(
        template_name='users/logged_out.html'), name='logout')
]
