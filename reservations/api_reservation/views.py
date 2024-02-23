from datetime import datetime
from django.shortcuts import render
import json
from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from ..models import Room, Reservation
from ..serializers import RoomSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..serializers import RoomSerializer


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
