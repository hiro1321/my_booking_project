import re
from dataclasses import dataclass
from datetime import datetime
from django.utils.timezone import make_aware
from ..models import Room, Reservation, Customer


@dataclass
class ReservationInputData:
    room_number: str
    checkin_date: datetime
    checkout_date: datetime
    name: str
    address: str
    phone_number: str
    email: str

    def __init__(
        self,
        room_number: str,
        checkin_date: str,
        checkout_date: str,
        checkin_time: str,
        checkout_time: str,
        name: str,
        address: str,
        phone_number: str,
        email: str,
    ):
        self.room_number = room_number

        checkin_dt = datetime.strptime(
            checkin_date + "T" + checkin_time, "%Y-%m-%dT%H:%M"
        )
        self.checkin_date = make_aware(checkin_dt)

        checkout_dt = datetime.strptime(
            checkout_date + "T" + checkout_time, "%Y-%m-%dT%H:%M"
        )
        self.checkout_date = make_aware(checkout_dt)

        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email

    def validate(self) -> list[str]:
        err_list: list[str] = []

        # 名前が空でないことをチェック
        if not self.name:
            err_list.append("名前を入力してください。")

        # 住所が空でないことをチェック
        if not self.address:
            err_list.append("住所を入力してください。")

        # 電話番号の形式をチェック
        if not re.match(r"^[0-9]{10,11}$", self.phone_number):
            err_list.append("有効な電話番号を入力してください。")

        # メールアドレスの形式をチェック
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email
        ):
            err_list.append("有効なメールアドレスを入力してください。")

        # チェックアウト日がチェックイン日の後であることをチェック
        if self.checkout_date <= self.checkin_date:
            err_list.append(
                "チェックアウト日はチェックイン日の後にする必要があります。"
            )

        # 選択した部屋の存在チェック
        room_count = Room.objects.filter(room_number=self.room_number).count()
        if room_count == 0:
            err_list.append("対象の部屋は存在しません。")
            # 処理を終了
            return err_list

        # 対象の日付に空きをチェック
        reservation_count = Reservation.objects.filter(
            room=Room.objects.get(room_number=self.room_number),
            start_datetime__lt=self.checkout_date,  # 予約の開始日がチェックアウト日よりも前
            end_datetime__gt=self.checkin_date,  # 予約の終了日がチェックイン日よりも後
        ).count()
        if reservation_count > 0:
            err_list.append("対象の日付で空きがありません。日付を変更してください。")

        return err_list

    def create_customer(self) -> Customer:
        return Customer.objects.create(
            name=self.name,
            address=self.address,
            phone=self.phone_number,
            email=self.email,
        )

    def create_reservation(self, customer: Customer) -> Reservation:
        return Reservation.objects.create(
            customer=customer,
            room=Room.objects.get(room_number=self.room_number),
            start_datetime=self.checkin_date,
            end_datetime=self.checkout_date,
            payment_info="現地で支払う",
        )
