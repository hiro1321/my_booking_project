from django.shortcuts import render
import json
from django.http.response import JsonResponse
from rest_framework.generics import ListAPIView
from .models import Room
from .serializers import RoomSerializer


# Create your views here.
def get_rooms(request):
    """
    homeのView
    """
    if request.method == "GET":
        return JsonResponse({"message": "get"})

        # JSON文字列
    datas = json.loads(request.body)

    # requestには、param1,param2の変数がpostされたものとする
    ret = {"data": "param1:" + datas["param1"] + ", param2:" + datas["param2"]}
    return JsonResponse()


class RoomListView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
