from dataclasses import dataclass
from datetime import datetime
from ..models import Reservation


@dataclass
class ReservationFormObject:
    """予約情報_画面表示用のオブジェクト"""

    id: int
    customer_id: int
    customer_name: str
    customer_phone: str
    customer_email: str
    customer_address: str
    room_id: int
    room_number: str
    room_type: str
    room_price: float
    room_availability: bool
    start_datetime: datetime
    end_datetime: datetime
    payment_info: str
    is_paid: bool

    def __init__(self, reservation: Reservation):
        self.id = reservation.id
        self.customer_id = reservation.customer.id
        self.customer_name = reservation.customer.name
        self.customer_phone = reservation.customer.phone
        self.customer_email = reservation.customer.email
        self.customer_address = reservation.customer.address
        self.room_id = reservation.room.id
        self.room_number = reservation.room.room_number
        self.room_type = reservation.room.room_type
        self.room_price = float(reservation.room.price)
        self.room_availability = reservation.room.availability
        self.start_datetime = reservation.start_datetime
        self.end_datetime = reservation.end_datetime
        self.payment_info = reservation.payment_info
        self.is_paid = reservation.is_paid
