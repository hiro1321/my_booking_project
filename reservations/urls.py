from django.urls import path
from .api_common import views as common_vi
from .api_admin import views as admin_vi

urlpatterns = [
    path("rooms", common_vi.RoomListView.as_view(), name="room_list"),
    path("rooms/<int:room_id>/", common_vi.room_detail, name="room_details"),
    path("csrf-token", common_vi.csrf_token, name="get_csrf_token"),
    path("admin/login", admin_vi.admin_login, name="admin_login"),
    path("admin/verify-token", admin_vi.verify_token, name="verify_token"),
    path("admin/logout", admin_vi.admin_logout, name="admin_logout"),
]
