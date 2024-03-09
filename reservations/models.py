from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()


class Room(models.Model):
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=50)
    room_image = models.ImageField(upload_to="room_images/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.room_number


class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    payment_info = models.TextField()
    is_paid = models.BooleanField(default=False)


class Payment(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_datetime = models.DateTimeField()
    payment_method = models.CharField(max_length=50)
