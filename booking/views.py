from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Hotel, Room, Booking
from .forms import BookingForm
from django.db.models import Q


def home(request):
    query = request.GET.get("q", "")

    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    return render(
        request,
        "home.html",
        {
            "hotels": hotels,
            "query": query,
        }
    )

def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)

    context = {
        "hotel": hotel,
        "rooms": rooms,
    }

    return render(request, "rooms.html", context)


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return render(
        request,
        "room_detail.html",
        {"room": room}
    )


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.user = request.user
            booking.room = room

            # Calculate total price
            nights = (booking.check_out - booking.check_in).days
            booking.total_price = nights * room.price

            if booking.guests > room.capacity:
                form.add_error(
                    "guests",
                    f"This room can only accommodate {room.capacity} guests."
                )

            else:
                already_booked = Booking.objects.filter(
                    room=room,
                    status__in=["Pending", "Confirmed"],
                    check_in__lt=booking.check_out,
                    check_out__gt=booking.check_in,
                ).exists()

                if already_booked:
                    form.add_error(
                        None,
                        "This room is already booked for these dates."
                    )

                else:
                    booking.save()

                    return redirect("booking_success")

    else:
        form = BookingForm()

    return render(
        request,
        "booking_form.html",
        {
            "room": room,
            "form": form,
        }
    )


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_bookings.html",
        {"bookings": bookings}
    )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == "POST":
        booking.status = "Cancelled"
        booking.save()

    return redirect("my_bookings")

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Hotel, Room, Booking
from .forms import BookingForm


def home(request):
    hotels = Hotel.objects.all()
    return render(request, "home.html", {"hotels": hotels})


def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    rooms = Room.objects.filter(hotel=hotel)

    context = {
        "hotel": hotel,
        "rooms": rooms,
    }

    return render(request, "rooms.html", context)


def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    return render(
        request,
        "room_detail.html",
        {"room": room}
    )


@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = BookingForm(request.POST)

        if form.is_valid():
            booking = form.save(commit=False)

            booking.user = request.user
            booking.room = room

            # Calculate total price
            nights = (booking.check_out - booking.check_in).days
            booking.total_price = nights * room.price

            if booking.guests > room.capacity:
                form.add_error(
                    "guests",
                    f"This room can only accommodate {room.capacity} guests."
                )

            else:
                already_booked = Booking.objects.filter(
                    room=room,
                    status__in=["Pending", "Confirmed"],
                    check_in__lt=booking.check_out,
                    check_out__gt=booking.check_in,
                ).exists()

                if already_booked:
                    form.add_error(
                        None,
                        "This room is already booked for these dates."
                    )

                else:
                    booking.save()

                    return redirect("booking_success")

    else:
        form = BookingForm()

    return render(
        request,
        "booking_form.html",
        {
            "room": room,
            "form": form,
        }
    )

@login_required
def booking_success(request):
    return render(request, "booking_success.html")

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "my_bookings.html",
        {"bookings": bookings}
    )

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(
        request,
        "register.html",
        {"form": form}
    )


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "login.html",
        {"form": form}
    )


def logout_view(request):
    logout(request)
    return redirect("home")

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if request.method == "POST":
        booking.status = "Cancelled"
        booking.save()

    return redirect("my_bookings")

@login_required
def booking_success(request):
    booking = Booking.objects.filter(user=request.user).order_by("created_at").first
    return render(request,"booking_success.html",{"booking":booking})@login_required
def booking_success(request):
    booking = Booking.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    return render(
        request,
        "booking_success.html",
        {
            "booking": booking
        }
    )