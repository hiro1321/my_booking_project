import os
from django.conf import settings
from datetime import datetime
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import Room, Reservation
from django.http import JsonResponse
from django.http import HttpResponse
from ..helpers.reservation_input_obj import ReservationInputData
from django.db import transaction
from django.shortcuts import get_object_or_404
from .forms import ReservationForm
from openpyxl import load_workbook
import tempfile

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


@api_view(["POST"])
def reservation_ispaid_edit(request, reservation_id):
    data: dict = request.data
    is_paid: bool = data.get("is_paid")
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.is_paid = is_paid
    reservation.save()

    return JsonResponse(
        {
            "message": "支払状態の更新に成功しました",
            "reservation_id": reservation_id,
        },
        status=200,
    )


def get_reception_file(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)

    # Excelファイルのパスを取得
    template_file_name = "reception-template.xlsx"
    template_file_path = os.path.join(
        settings.BASE_DIR, "templates", template_file_name
    )

    # テンプレートの読み込み
    workbook = load_workbook(template_file_path)
    sheet = workbook.active

    # 予約情報を書き込む
    sheet["A3"] = reservation.customer.name
    sheet["B11"] = reservation.room.room_number
    sheet["B12"] = reservation.start_datetime.strftime("%Y-%m-%d %H:%M:%S")
    sheet["B13"] = reservation.end_datetime.strftime("%Y-%m-%d %H:%M:%S")

    # 一時ディレクトリの作成
    temp_dir = tempfile.mkdtemp()

    # Excelファイルを保存
    response_file_path = os.path.join(temp_dir, "reception-output.xlsx")
    workbook.save(response_file_path)

    # レスポンスを作成し、Excelファイルを返す
    with open(response_file_path, "rb") as f:
        response = HttpResponse(
            f.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response["Content-Disposition"] = 'attachment; filename="reception-output.xlsx"'

    return response
