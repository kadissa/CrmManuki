from django.urls import path
from . import views

app_name = 'bnovo'


urlpatterns = [
    path('', views.TodayListView.as_view(), name='today_list'),
    path('<date>/', views.TodayListView.as_view(), name='any_day'),

    path('sauna/<int:pk>/', views.SaunaDetailView.as_view(),
         name='sauna_detail'),
    path('chale/<int:pk>/', views.ChaleDetailView.as_view(),
         name='chale_detail')

]
