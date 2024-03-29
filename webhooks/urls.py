from django.urls import path
from . import views

app_name = 'webhooks'

urlpatterns = [
    path('', views.easyweek_hook, name='webhooks'),
]
