from django.urls import path
from .api_common import views


urlpatterns = [
    path("rooms", views.RoomListView.as_view(), name="room-list"),
    path("admin/login", views.RoomListView.as_view(), name="room-list"),
]
