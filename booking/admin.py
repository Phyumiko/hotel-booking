from django.contrib import admin
from .models import Hotel, Room, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hotel', 'room_type','price', 'capacity',)
    list_filter = ('hotel', 'room_type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'check_in', 'check_out', 'guests', 'status',)
    list_filter = ('status',)
    list_editable = ("status",)
    search_fields = ("user__username", "room__room_number", "room__hotel__name",)
