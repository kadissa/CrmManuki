from django.urls import path
from . import views

app_name = 'bnovo'


urlpatterns = [
    # path('', views.guest_cart_on_today_view)
    path('', views.TodayListView.as_view(), name='today_list'),
    path('sauna/<int:pk>/', views.SaunaDetailView.as_view(),
         name='sauna_detail'),
    path('chale/<int:pk>/', views.ChaleDetailView.as_view(),
         name='chale_detail')

]
