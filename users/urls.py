from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'users'

urlpatterns = [
    path('logout/', views.logout_view, name='logout'),
    path('login/', LoginView.as_view(template_name='users/login.html'),
         name='login'),
    # path('<booking_id>/<sauna_price>/', views.guest_self_edit,
    #      name='self_edit'),
    # path('success_url/<pk>', views.get_success, name='success_url')
]
