from django.urls import path
from .api_common import views as common_vi
from .api_admin import views as admin_vi
from .api_reservation import views as res_vi

urlpatterns = [
    path("csrf-token", common_vi.csrf_token, name="get_csrf_token"),
    path("rooms", common_vi.RoomListView.as_view(), name="room_list"),
    path("rooms/<int:room_id>/", common_vi.room_detail, name="room_details"),
    path("rooms/submit/", common_vi.room_submit, name="room_submit"),
    path(
        "reservations/availability-cnt/<str:date>/",
        res_vi.getRoomAvailability,
        name="availability_cnt",
    ),
    path(
        "reservations/submit",
        res_vi.submitReservation,
        name="submit_reservation",
    ),
    path("reservations/", res_vi.reservation_list, name="reservation_list"),
    path(
        "reservations/<int:reservation_id>/",
        res_vi.reservation_detail,
        name="reservation_detail",
    ),
    path("reservations/create/", res_vi.reservation_create, name="reservation_create"),
    path(
        "reservations/<int:reservation_id>/edit/",
        res_vi.reservation_edit,
        name="reservation_edit",
    ),
    path(
        "reservations/<int:reservation_id>/delete/",
        res_vi.reservation_delete,
        name="reservation_delete",
    ),
    path(
        "reservations/<int:reservation_id>/is_paid/edit/",
        res_vi.reservation_ispaid_edit,
        name="reservation_ispaid_edit",
    ),
    path(
        "reservations/<int:reservation_id>/get_reception_file/",
        res_vi.get_reception_file,
        name="get_reception_file",
    ),
    path("admin/login", admin_vi.admin_login, name="admin_login"),
    path("admin/verify-token", admin_vi.verify_token, name="verify_token"),
    path("admin/logout", admin_vi.admin_logout, name="admin_logout"),
]
