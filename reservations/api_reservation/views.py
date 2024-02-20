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
    """対象日付の予約可能な部屋数を返す"""
    # 予約可能な部屋の数を取得
    room_cnt = Room.objects.filter(availability=True).count()

    # 予約が埋まっている数を取得
    date_obj = datetime.strptime(date, "%Y%m%d")
    reservation_count = Reservation.objects.filter(
        start_datetime__lte=date_obj, end_datetime__gte=date_obj
    ).count()

    result = room_cnt - reservation_count
    print(result)
    return JsonResponse({"result": result})


def room_detail(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)

    if request.method == "GET":
        serializer = RoomSerializer(room)
        return JsonResponse(serializer.data)

    elif request.method == "PUT":
        data = json.loads(request.body.decode("utf-8"))
        serializer = RoomSerializer(room, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)
