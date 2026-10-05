from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single Room'),
        ('Double', 'DOuble Room'),
        ('Delux', 'Delux Room'),
        ('Suite', ' Suite'),
    ]

    hotel =models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='rooms')
    room_number = models.CharField(max_length=20)
    room_type = models.CharField(max_length=20,choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    def __str__(self):
        return f"{self.hotel.name} - Room{self.room_number}"

class Booking(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Confirmed', 'COnfirmed'),('Cancelled', 'Cancelled'),] 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    total_price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True )
    def __str__(self):
        return f"{self.user.username} - {self.room}"