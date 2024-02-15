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
        serializer = RoomSerializer(room)
        response = JsonResponse(serializer.data)
        return response
    except Room.DoesNotExist:
        return JsonResponse({"error": "Room not found"}, status=404)
