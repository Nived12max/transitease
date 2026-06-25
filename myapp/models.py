from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    rollno=models.IntegerField()
    dept=models.CharField(max_length=40)
    
class emp(models.Model):
    name=models.CharField(max_length=20)
    salary=models.IntegerField()
    








def generate_booking_id():
    return str(uuid.uuid4())[:8].upper()


class Booking(models.Model):
    
    bus = models.ForeignKey(
    'Bus',
    on_delete=models.CASCADE,
    null=True,
    blank=True
)


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    booking_id = models.CharField(
        max_length=20,
        unique=True,
        default=generate_booking_id
    )

    bus_name = models.CharField(
        max_length=100
    )

    journey_date = models.CharField(
        max_length=20
    )

    # Multiple seats in one ticket
    seat_no = models.TextField()

    # Multiple passengers in one ticket
    passenger_name = models.TextField()

    phone = models.CharField(
        max_length=15
    )

    payment_status = models.CharField(
        max_length=20,
        default="Pending"
    )

    boarding_point = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    boarding_time = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    drop_point = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    drop_time = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    total_fare = models.IntegerField(
        default=0
    )

    booked_on = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.booking_id} - {self.passenger_name}"
    
class Route(models.Model):

    from_city = models.CharField(
        max_length=100
    )

    to_city = models.CharField(
        max_length=100
    )

    def __str__(self):
        return f"{self.from_city} → {self.to_city}"
    
class Bus(models.Model):

    name = models.CharField(
        max_length=100,
        default=""
    )

    bus_number = models.CharField(
        max_length=20,
        default=""
    )

    bus_type = models.CharField(
        max_length=20,
        default=""
    )

    route = models.TextField(
        default=""
    )

    route_obj = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    departure_time = models.CharField(
        max_length=20,
        default=""
    )

    arrival_time = models.CharField(
        max_length=20,
        default=""
    )

    fare = models.IntegerField(
        default=0
    )

    driver_name = models.CharField(
        max_length=100,
        default=""
    )

    driver_phone = models.CharField(
        max_length=15,
        default=""
    )

    tracking_link = models.URLField(
        blank=True,
        null=True
    )

    current_location = models.CharField(
        max_length=100,
        default="Depot"
    )

    status = models.CharField(
        max_length=20,
        default="Running"
    )

    latitude = models.FloatField(
        default=12.9716
    )

    longitude = models.FloatField(
        default=77.5946
    )

    next_stop = models.CharField(
        max_length=100,
        default=""
    )

    eta = models.CharField(
        max_length=50,
        default=""
    )



    def __str__(self):
        return self.name

class Complaint(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    complaint_id = models.CharField(
        max_length=20,
        unique=True,
        default=generate_booking_id
    )

    subject = models.CharField(
        max_length=200
    )

    message = models.TextField()

    status = models.CharField(
        max_length=20,
        default="Pending"
    )

    admin_reply = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.subject


class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.message[:50]
    

class LoginHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    login_time = models.DateTimeField(
        auto_now_add=True
    )

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username