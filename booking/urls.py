from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path(
        "hotel/<int:hotel_id>/rooms/",
        views.room_list,
        name="room_list"
    ),
    path(
        "room/<int:room_id>/",
        views.room_detail,
        name="room_detail"
    ),
    path(
        "room/<int:room_id>/book/",
        views.book_room,
        name ="book_room"
    ),
    path(
        "booking/success/",views.booking_success,name="booking_success"
    ),
    path("my_bookings/",views.my_bookings,name="my_bookings"),
    path("register/",views.register,name="register"),
    path("login/",views.login_view,name="login"),
    path("logout/",views.logout_view,name="logout"),
    path("booking/<int:booking_id>/cancel/",views.cancel_booking,name="cancel_booking"),
]