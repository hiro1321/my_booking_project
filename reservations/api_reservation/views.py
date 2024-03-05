from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Room, Reservation
from django.http import JsonResponse
from ..helpers.reservation_input_obj import ReservationInputData
from django.db import transaction
from django.shortcuts import get_object_or_404
from .forms import ReservationForm
from django.forms.models import model_to_dict
from ..helpers.reservation_form_obj import ReservationFormObject


@api_view(["GET"])
def getRoomAvailability(request, date):
    """
    指定された日付における部屋の空き状況を取得するAPIエンドポイント。

    Parameters:
        request (HttpRequest): HTTPリクエストオブジェクト。
        date (str): 日付を表す文字列（YYYYMMDD形式）。

    Returns:
        JsonResponse: 空き部屋の数を含むJSON形式のレスポンス。

    Raises:
        ValueError: date引数が無効な日付形式の場合に発生。
    """
    # 予約可能な部屋の数を取得
    room_cnt = Room.objects.filter(availability=True).count()

    # 予約が埋まっている数を取得
    date_obj = datetime.strptime(date, "%Y%m%d")
    reservation_count = Reservation.objects.filter(
        start_datetime__lte=date_obj, end_datetime__gte=date_obj
    ).count()

    result = room_cnt - reservation_count
    return JsonResponse({"result": result})


@api_view(["POST"])
def submitReservation(request):
    #  入力データをチェック
    data: dict = request.data
    reservation_input_data = ReservationInputData(request_data=data, reservation_id="")
    error_list = reservation_input_data.validate()

    # エラーがある場合、ステータス400で終了
    if len(error_list) != 0:
        return Response({"errors": error_list}, status=400)

    # Customerオブジェクトを作成
    customer = reservation_input_data.create_customer()

    try:
        # トランザクションを開始して顧客と予約を保存
        with transaction.atomic():
            customer.save()
            reservation = reservation_input_data.create_reservation(customer)
            reservation.save()
    except Exception as e:
        # エラーが発生した場合はロールバック
        customer.delete()
        return Response({"errors": ["予約登録中にエラーが発生しました"]}, status=400)

    # レスポンスを返す
    return Response({"message": "success"}, status=201)


def reservation_list(request):
    print("start debug")
    if request.method == "GET":
        reservations = Reservation.objects.all().select_related("customer", "room")
        reservation_data = [
            ReservationFormObject(reservation).__dict__ for reservation in reservations
        ]
        return JsonResponse({"reservations": reservation_data})


@api_view(["GET"])
def reservation_detail(request, reservation_id):
    """予約IDをもとに、予約情報を返却"""
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    data = {"reservation": ReservationFormObject(reservation).__dict__}
    return JsonResponse(data)


@api_view(["POST"])
def reservation_create(request):
    form = ReservationForm(request.POST)
    if form.is_valid():
        reservation = form.save()
        return JsonResponse(
            {
                "message": "Reservation created successfully",
                "reservation_id": reservation.id,
            },
            status=201,
        )


@api_view(["POST"])
def reservation_edit(request, reservation_id):
    data: dict = request.data
    reservation_input_data = ReservationInputData(data, reservation_id)
    error_list = reservation_input_data.validate()

    # エラーがある場合、ステータス400で終了
    if len(error_list) != 0:
        print(error_list)
        return Response({"errors": error_list}, status=400)

    reservation_input_data.update_reservation()
    return JsonResponse(
        {
            "message": "Reservation created successfully",
            "reservation_id": reservation_id,
        },
        status=200,
    )


@api_view(["DELETE"])
def reservation_delete(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    reservation.delete()
    return JsonResponse({"message": "success"})
