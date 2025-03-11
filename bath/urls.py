from django.urls import path
from bath import views

appname = "bath"

urlpatterns = [
    path("", views.get_customer_and_date, name="user"),
    path("cart/<int:pk>", views.cart_detail, name="cart"),
    path("products/<int:pk>", views.add_items, name="products"),
    path(
        "appointment/<str:day>/<int:user_id>",
        views.create_appointment,
        name="create_appointment",
    ),
    path(
        "confirm_date_time/<int:appoint_id>",
        views.confirm_date_time,
        name="confirm_date_time",
    ),
    path("time/<str:day>/<int:user_id>", views.get_time_slots, name="time"),
    path("error/", views.error, name="error"),
    path("cart_remove/<int:pk>", views.clear_cart, name="cart_remove"),
    path("rotenburo_times/<int:pk>", views.get_rotenburo_times, name="rotenburo_times"),
    path("add_rotenburo/<int:pk>", views.add_rotenburo, name="add_rotenburo"),
]
