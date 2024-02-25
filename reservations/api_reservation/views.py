from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Room, Reservation, Customer
from django.utils.timezone import make_aware
from django.http import JsonResponse
from ..helpers.reservation_input_obj import ReservationInputData
from django.db import transaction


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
    data = request.data
    print(data)
    reservation_input_data = ReservationInputData(
        room_number=data.get("roomNumber"),
        checkin_date=data.get("checkInDate"),
        checkout_date=data.get("checkOutDate"),
        checkin_time=data.get("checkInTime"),
        checkout_time=data.get("checkOutTime"),
        name=data.get("name"),
        address=data.get("address"),
        phone_number=data.get("phoneNumber"),
        email=data.get("email"),
    )
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
