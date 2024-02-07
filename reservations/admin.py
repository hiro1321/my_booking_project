from django.contrib import admin
from .models import Customer, Room, Reservation, Payment

# Register your models here.
admin.site.register(Customer)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Payment)
