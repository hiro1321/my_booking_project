from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
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
        serializer = RoomSerializer(room, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)
