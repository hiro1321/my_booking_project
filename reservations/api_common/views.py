import json
import base64
from django.shortcuts import render
from django.http.response import JsonResponse
from django.core.files.base import ContentFile
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from ..models import Room
from ..serializers import RoomSerializer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token
from ..serializers import RoomSerializer


@csrf_exempt
def csrf_token(request):
    if request.method == "GET":
        token = get_token(request)
        print(token)
        return JsonResponse({"csrfToken": token})
    else:
        return JsonResponse({"error": "CSRFトークンを取得できませんでした"}, status=400)


class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


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
        room = Room.objects.get(pk=room_id)
        room.room_number = data.get("room_number")
        room.room_type = data.get("room_type")
        room.price = float(data.get("price"))
        room.availability = True
        room_image_base64 = data["room_image"]
        room_image_data = base64.b64decode(room_image_base64)
        room.room_image.save("room_image.png", ContentFile(room_image_data))
        room.save()

        return JsonResponse({"message": "Room data saved successfully"})


@api_view(["POST"])
def room_submit(request):
    data: dict = request.data
    room = Room(
        room_number=data.get("room_number"),
        room_type=data.get("room_type"),
        price=data.get("price"),
        availability=(True),
    )
    room.save()
    # 登録された Room の情報をレスポンスとして返す
    return JsonResponse({"message": "Room data saved successfully"})
