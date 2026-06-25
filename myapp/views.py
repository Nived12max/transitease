from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Student
from .models import emp
from .forms import StudentForm
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Booking
from django.contrib.auth.decorators import login_required
from .models import Booking
from reportlab.pdfgen import canvas
from .models import Booking, Bus
from .models import Complaint
from .models import Notification
from .models import Route
from .models import LoginHistory
from django.db.models import Count, Sum
from django.core.mail import send_mail


# Create your views here.
def sample(request):
    return HttpResponse('hi')
def demo(request):
    return HttpResponse('hellooooo')

def demo1(request):
    return render(request,'myapp/sample.html')
def demo2(request):
    return render(request,'myapp/niv.html')

def demo3(request):
    return render(request,'myapp/img.html')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'myapp/students.html', {'students': students})


def emp1(request):
    employee=emp.objects.all()
    return render(request,'myapp/employeee.html',{'employee':employee})



def student_form(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('showstudents')

    else:
        form = StudentForm()

    return render(request, 'myapp/studentform.html', {'form': form})


def show_students(request):

    students = Student.objects.all()

    return render(request, 'myapp/students.html', {'students': students})


def edit_student(request,id):
    student = get_object_or_404(Student,id=id)

    if request.method == "POST":    
        student.name = request.POST['name']
        student.age = request.POST['age']
        student.rollno = request.POST['rollno']
        student.dept = request.POST['dept']

        student.save()

        return redirect('/show')

    return render(request,'myapp/edit.html',{'student':student})


def delete_student(request,id):

    student = get_object_or_404(Student,id=id)

    student.delete()

    return redirect('/show')




def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            LoginHistory.objects.create(
                user=user
            )

            return redirect('home')

        else:

            messages.error(
                request,
                "Username or Password is incorrect"
            )

    return render(
        request,
        'myapp/login.html'
    )


def logout_view(request):

    logout(request)

    return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')



def home(request):

    routes = Route.objects.all()

    return render(
        request,
        'myapp/home.html',
        {
            'routes': routes
        }
    )



from .models import Bus

from .models import Bus

def bus_list(request):

    origin = request.GET.get('origin', '').strip().lower()
    destination = request.GET.get('destination', '').strip().lower()
    date = request.GET.get('journey_date')

    filtered_buses = []

    buses = Bus.objects.all()

    for bus in buses:

        route_list = [
            stop.strip().lower()
            for stop in bus.route.split(',')
        ]

        if origin in route_list and destination in route_list:

            origin_index = route_list.index(origin)
            destination_index = route_list.index(destination)

            if origin_index < destination_index:

                filtered_buses.append(bus)

    return render(
        request,
        'myapp/bus_list.html',
        {
            'buses': filtered_buses,
            'origin': request.GET.get('origin'),
            'destination': request.GET.get('destination'),
            'date': date
        }
    )



def seat_selection(request):

    bus_type = request.GET.get('type')

    bus_name = request.session.get('bus_name')
    journey_date = request.session.get('journey_date')

    booked_seats = Booking.objects.filter(
        bus_name=bus_name,
        journey_date=journey_date
    ).values_list(
        'seat_no',
        flat=True
    )

    if bus_type == 'sleeper':

        return render(
            request,
            'myapp/sleeper.html',
            {
                'booked_seats': booked_seats
            }
        )

    elif bus_type == 'seater':

        return render(
            request,
            'myapp/seater.html',
            {
                'booked_seats': booked_seats
            }
        )

    return redirect('home')


def passenger_details(request):

    seats = request.GET.get('seats', '')

    seat_list = []

    if seats:
        seat_list = seats.split(',')

    return render(
        request,
        'myapp/passenger.html',
        {
            'seat_list': seat_list
        }
    )



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def booking_summary(request):

    if request.method == "POST":

        seats = request.POST.getlist("seat")

        if len(seats) > 6:

            messages.error(
                request,
                "Maximum 6 seats can be booked in a single transaction."
            )

            return redirect("home")

        names = request.POST.getlist("name")
        ages = request.POST.getlist("age")
        genders = request.POST.getlist("gender")
        phones = request.POST.getlist("phone")
        emails = request.POST.getlist("email")

        passengers = []

        for i in range(len(seats)):

            passengers.append({
                "seat": seats[i],
                "name": names[i],
                "age": ages[i],
                "gender": genders[i],
                "phone": phones[i],
                "email": emails[i]
            })

        fare = request.session.get("fare")

        if not fare:
            fare = 0

        try:
            fare_per_seat = int(fare)
        except:
            fare_per_seat = 0

        total_fare = len(seats) * fare_per_seat

        request.session["total_fare"] = total_fare

        request.session["booking_data"] = {
            "seats": seats,
            "names": names,
            "ages": ages,
            "genders": genders,
            "phones": phones,
            "emails": emails
        }

        return render(
            request,
            "myapp/summary.html",
            {
                "passengers": passengers,
                "fare_per_seat": fare_per_seat,
                "total_fare": total_fare,
                "bus_name": request.session.get(
                    "bus_name",
                    "SPONROKO"
                ),
                "journey_date": request.session.get(
                    "journey_date",
                    "-"
                ),
                "boarding_point": request.session.get(
                    "boarding_point",
                    "-"
                ),
                "drop_point": request.session.get(
                    "drop_point",
                    "-"
                )
            }
        )

    return redirect("home")



def support(request):
    return render(request, 'myapp/support.html')

def settings(request):
    return render(request, 'myapp/settings.html')

from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render

from django.shortcuts import render
from django.contrib.auth import update_session_auth_hash


from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import render

def settings(request):

    message = ""
    show_password_form = False

    if request.method == "POST":

        action = request.POST.get("action")

        if action == "update_profile":

            new_username = request.POST.get("username")
            new_email = request.POST.get("email")

            if User.objects.filter(
                username=new_username
            ).exclude(
                id=request.user.id
            ).exists():

                message = "Username already exists ❌"

            else:

                request.user.username = new_username
                request.user.email = new_email

                request.user.save()

                request.session["language"] = request.POST.get("language")

                message = "Profile updated successfully ✅"

        elif action == "show_password":

            show_password_form = True

        elif action == "change_password":

            show_password_form = True

            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")

            if request.user.check_password(old_password):

                request.user.set_password(new_password)
                request.user.save()

                update_session_auth_hash(
                    request,
                    request.user
                )

                message = "Password changed successfully ✅"

            else:

                message = "Current password is incorrect ❌"

    return render(
        request,
        "myapp/settings.html",
        {
            "message": message,
            "show_password_form": show_password_form
        }
    )


@login_required
def profile(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booked_on')

    return render(
        request,
        "myapp/profile.html",   # ✅ Correct
        {
            "bookings": bookings
        }
    )
    

        


def support(request):

    return render(request,'myapp/support.html')







from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-booked_on')

    return render(
        request,
        'myapp/my_bookings.html',
        {'bookings': bookings}
    )


from django.shortcuts import render, get_object_or_404
from .models import Booking
import qrcode
import base64
from io import BytesIO
@login_required
def ticket(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    qr = qrcode.make(booking.booking_id)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_code = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return render(
        request,
        'myapp/ticket.html',
        {
            'booking': booking,
            'qr_code': qr_code
        }
    )


@login_required
def cancel_booking(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    booking.delete()

    return redirect('profile')

@login_required
@login_required
def payment(request):

    booking_data = request.session.get("booking_data")

    if not booking_data:
        return redirect("home")

    fare_per_seat = int(
        request.session.get("fare", 0)
    )

    total_fare = len(
        booking_data["seats"]
    ) * fare_per_seat

    upi_link = (
        f"upi://pay?"
        f"pa=nivedragesh22@oksbi"
        f"&pn=SPONROKO Travels"
        f"&am={total_fare}"
        f"&cu=INR"
    )

    return render(
        request,
        "myapp/payment.html",
        {
            "total_fare": total_fare,
            "upi_link": upi_link
        }
    )

from django.core.mail import send_mail


@login_required
def payment_success(request):

    if request.method != "POST":
        return redirect("payment")

    booking_data = request.session.get(
        "booking_data"
    )

    if booking_data is None:
        return redirect("payment")

    seats = booking_data["seats"]

    names = booking_data["names"]

    phones = booking_data["phones"]

    emails = booking_data["emails"]

    total_fare = request.session.get(
        "total_fare",
        0
    )

    selected_bus = Bus.objects.filter(

        name=request.session.get(
            "bus_name"
        )

    ).first()

    booking = Booking.objects.create(

        user=request.user,

        bus=selected_bus,

        bus_name=request.session.get(
            "bus_name",
            ""
        ),

        journey_date=request.session.get(
            "journey_date",
            ""
        ),

        seat_no=", ".join(seats),

        passenger_name=", ".join(names),

        phone=phones[0],

        payment_status="Paid",

        boarding_point=request.session.get(
            "boarding_point",
            ""
        ),

        boarding_time=request.session.get(
            "departure_time",
            ""
        ),

        drop_point=request.session.get(
            "drop_point",
            ""
        ),

        drop_time=request.session.get(
            "arrival_time",
            ""
        ),

        total_fare=total_fare

    )

    # Send email

    if emails:

        send_mail(

            subject="🎫 SPONROKO Travels Ticket Confirmation",

            message=f"""

Hello,

Your booking has been confirmed.

Booking ID : {booking.booking_id}

Bus : {booking.bus_name}

Journey Date : {booking.journey_date}

Passengers : {booking.passenger_name}

Seats : {booking.seat_no}

Boarding Point : {booking.boarding_point}

Boarding Time : {booking.boarding_time}

Drop Point : {booking.drop_point}

Arrival Time : {booking.drop_time}

Total Fare : ₹{booking.total_fare}

Thank you for choosing SPONROKO Travels.

Have a safe journey.

SPONROKO Travels

""",

            from_email=None,

            recipient_list=emails,

            fail_silently=False

        )

    request.session.pop(
        "booking_data",
        None
    )

    return redirect(
        "ticket",
        id=booking.id
    )
from reportlab.lib.utils import ImageReader
from datetime import datetime
import qrcode
import io

@login_required
def download_ticket(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="SPONROKO_{booking.booking_id}.pdf"'
    )

    p = canvas.Canvas(response)

    p.setTitle("SPONROKO Ticket")

    # =====================
    # HEADER
    # =====================

    p.setFillColorRGB(0.8, 0, 0)
    p.rect(0, 770, 600, 70, fill=1)

    p.setFillColorRGB(1, 1, 1)
    p.setFont("Helvetica-Bold", 22)

    p.drawString(
        150,
        795,
        "SPONROKO TRAVELS"
    )

    # =====================
    # ROUTE BOX
    # =====================

    p.setFillColorRGB(0.95, 0.95, 0.95)

    p.rect(
        40,
        680,
        520,
        60,
        fill=1
    )

    p.setFillColorRGB(0, 0, 0)

    p.setFont(
        "Helvetica-Bold",
        16
    )

    p.drawString(
        80,
        705,
        booking.boarding_point.upper()
    )

    p.drawString(
        280,
        705,
        "→"
    )

    p.drawString(
        360,
        705,
        booking.drop_point.upper()
    )

    # =====================
    # BOOKING DETAILS
    # =====================

    p.roundRect(
        40,
        500,
        520,
        150,
        10
    )

    p.setFont(
        "Helvetica",
        12
    )

    p.drawString(
        60,
        620,
        f"Booking ID : {booking.booking_id}"
    )

    p.drawString(
        60,
        595,
        f"Passengers : {booking.passenger_name}"
    )

    p.drawString(
        60,
        570,
        f"Seats : {booking.seat_no}"
    )

    p.drawString(
        60,
        545,
        f"Bus : {booking.bus_name}"
    )

    p.drawString(
        60,
        520,
        f"Journey Date : {booking.journey_date}"
    )

    # =====================
    # BOARDING
    # =====================

    p.roundRect(
        40,
        340,
        240,
        120,
        10
    )

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        60,
        430,
        "BOARDING"
    )

    p.setFont(
        "Helvetica",
        11
    )

    p.drawString(
        60,
        400,
        booking.boarding_point[:50]
    )

    p.drawString(
        60,
        375,
        f"Time : {booking.boarding_time}"
    )

    # =====================
    # DROPPING
    # =====================

    p.roundRect(
        320,
        340,
        240,
        120,
        10
    )

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        340,
        430,
        "DROPPING"
    )

    p.setFont(
        "Helvetica",
        11
    )

    p.drawString(
        340,
        400,
        booking.drop_point[:50]
    )

    p.drawString(
        340,
        375,
        f"Time : {booking.drop_time}"
    )

    # =====================
    # FARE BOX
    # =====================

    p.setFillColorRGB(
        0,
        0.6,
        0
    )

    p.roundRect(
        40,
        260,
        520,
        50,
        10,
        fill=1
    )

    p.setFillColorRGB(
        1,
        1,
        1
    )

    p.setFont(
        "Helvetica-Bold",
        18
    )

    p.drawString(
        170,
        280,
        f"TOTAL FARE : ₹{booking.total_fare}"
    )

    # =====================
    # PAID BADGE
    # =====================

    p.setFillColorRGB(
        0,
        0.6,
        0
    )

    p.roundRect(
        180,
        205,
        220,
        35,
        8,
        fill=1
    )

    p.setFillColorRGB(
        1,
        1,
        1
    )

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        220,
        218,
        "✓ PAID & CONFIRMED"
    )

    # =====================
    # QR CODE
    # =====================

    qr_data = f"""
Booking ID: {booking.booking_id}
Passenger: {booking.passenger_name}
Seats: {booking.seat_no}
Date: {booking.journey_date}
Bus: {booking.bus_name}
"""

    qr = qrcode.make(qr_data)

    buffer = io.BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    p.drawImage(
        ImageReader(buffer),
        420,
        70,
        width=100,
        height=100
    )

    # =====================
    # EXTRA DETAILS
    # =====================

    p.setFillColorRGB(
        0,
        0,
        0
    )

    p.setFont(
        "Helvetica",
        10
    )

    p.drawString(
        50,
        160,
        f"Contact Number : {booking.phone}"
    )

    p.drawString(
        50,
        145,
        f"Generated On : {datetime.now().strftime('%d-%m-%Y %H:%M')}"
    )

    # =====================
    # FOOTER
    # =====================

    p.drawString(
        120,
        115,
        "Thank you for choosing SPONROKO Travels"
    )

    p.drawString(
        70,
        95,
        "SPONROKO Travels Logistics, Kalasipalyam, Bangalore"
    )

    p.drawString(
        70,
        80,
        "Customer Care : +91 9876543210"
    )

    p.save()

    return response

@login_required
def pickup_drop(request):

    route = request.GET.get("route", "")
    stops = route.split(",")

    # Save bus details immediately
    request.session["bus_name"] = request.GET.get("bus", "SPONROKO")
    request.session["fare"] = request.GET.get("fare", "0")
    request.session["departure_time"] = request.GET.get("departure", "")
    request.session["arrival_time"] = request.GET.get("arrival", "")
    request.session["journey_date"] = request.GET.get("date", "")

    if request.method == "POST":

        request.session["boarding_point"] = request.POST.get(
            "boarding_point"
        )

        request.session["drop_point"] = request.POST.get(
            "drop_point"
        )

        return redirect(
            f"/seats/?type={request.GET.get('type')}"
        )

    return render(
        request,
        "myapp/pickup_drop.html",
        {
            "stops": stops
        }
    )





@login_required
def verify_ticket(request):

    booking = None

    if request.method == "POST":

        booking_id = request.POST.get(
            "booking_id"
        )

        try:

            booking = Booking.objects.get(
                booking_id=booking_id
            )

        except Booking.DoesNotExist:

            booking = None

    return render(
        request,
        "myapp/verify_ticket.html",
        {
            "booking": booking
        }
    )



@login_required
def admin_panel(request):

    if not request.user.is_staff:
        return redirect('home')

    total_bookings = Booking.objects.count()

    total_revenue = sum(
        booking.total_fare
        for booking in Booking.objects.all()
    )

    total_passengers = 0

    for booking in Booking.objects.all():

        total_passengers += len(
            booking.passenger_name.split(',')
        )

    context = {

    'total_bookings': total_bookings,

    'total_revenue': total_revenue,

    'total_passengers': total_passengers,

    'recent_bookings':
        Booking.objects.all()
        .order_by('-booked_on')[:10],

    'buses':
        Bus.objects.all(),

    'routes':
        Route.objects.all()

}

    return render(
        request,
        'myapp/admin_panel.html',
        context
    )


@login_required
def add_bus(request):

    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":

        driver_phone = request.POST.get(
            "driver_phone"
        )

        if not driver_phone.isdigit():

            messages.error(
                request,
                "Driver phone must contain digits only"
            )

            return redirect(
                "add_bus"
            )

        if len(driver_phone) != 10:

            messages.error(
                request,
                "Driver phone must be exactly 10 digits"
            )

            return redirect(
                "add_bus"
            )

        Bus.objects.create(

            name=request.POST.get("name"),

            bus_number=request.POST.get("bus_number"),

            bus_type=request.POST.get("bus_type"),

            route=request.POST.get("route"),

            departure_time=request.POST.get("departure_time"),

            arrival_time=request.POST.get("arrival_time"),

            fare=request.POST.get("fare"),

            driver_name=request.POST.get("driver_name"),

            driver_phone=driver_phone

        )

        messages.success(
            request,
            "Bus added successfully"
        )

        return redirect(
            "admin_panel"
        )

    return render(
        request,
        "myapp/add_bus.html"
    )

@login_required
def edit_bus(request, id):

    if not request.user.is_staff:
        return redirect('home')
    bus = get_object_or_404(
        Bus,
        id=id
    )

    if request.method == "POST":

        bus.name = request.POST.get("name")

        bus.bus_number = request.POST.get(
            "bus_number"
        )

        bus.bus_type = request.POST.get(
            "bus_type"
        )

        bus.route = request.POST.get(
            "route"
        )

        bus.departure_time = request.POST.get(
            "departure_time"
        )

        bus.arrival_time = request.POST.get(
            "arrival_time"
        )

        bus.fare = request.POST.get(
            "fare"
        )

        bus.driver_name = request.POST.get(
            "driver_name"
        )

        bus.driver_phone = request.POST.get(
            "driver_phone"
        )

        bus.save()

        return redirect(
            "admin_panel"
        )

    return render(
        request,
        "myapp/edit_bus.html",
        {
            "bus": bus
        }
    )

@login_required
def delete_bus(request, id):

    if not request.user.is_staff:
        return redirect('home')

    bus = Bus.objects.get(id=id)

    bus.delete()

    return redirect('admin_panel')

@login_required
def complaints(request):

    if request.method == "POST":

        Complaint.objects.create(

            user=request.user,

            subject=request.POST.get(
                "subject"
            ),

            message=request.POST.get(
                "message"
            )

        )

        return redirect(
            "complaints"
        )

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "myapp/complaints.html",
        {
            "complaints": complaints
        }
    )

@login_required
def complaints(request):

    if request.method == "POST":

        Complaint.objects.create(

            user=request.user,

            subject=request.POST.get(
                "subject"
            ),

            message=request.POST.get(
                "message"
            )

        )

        return redirect(
            "complaints"
        )

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "myapp/complaints.html",
        {
            "complaints": complaints
        }
    )

@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "myapp/notifications.html",
        {
            "notifications": notifications
        }
    )

@login_required
def admin_complaints(request):

    if not request.user.is_staff:
        return redirect("home")

    complaints = Complaint.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "myapp/admin_complaints.html",
        {
            "complaints": complaints
        }
    )

@login_required
def reply_complaint(request, id):

    if not request.user.is_staff:
        return redirect("home")

    complaint = get_object_or_404(
        Complaint,
        id=id
    )

    if request.method == "POST":

        reply = request.POST.get(
            "reply"
        )

        complaint.admin_reply = reply

        complaint.status = "Replied"

        complaint.save()

        Notification.objects.create(

            user=complaint.user,

            message=
            f"Admin replied to complaint "
            f"{complaint.complaint_id}: "
            f"{reply}"

        )

        return redirect(
            "admin_complaints"
        )

    return render(
        request,
        "myapp/reply_complaint.html",
        {
            "complaint": complaint
        }
    )

@login_required
def track_bus(request, id):

    booking = get_object_or_404(
        Booking,
        id=id,
        user=request.user
    )

    if not booking.bus:

        return HttpResponse(
            "No bus linked with this booking."
        )

    return render(
        request,
        "myapp/track_bus.html",
        {
            "booking": booking,
            "bus": booking.bus
        }
    )


@login_required
def update_location(request, id):

    if not request.user.is_staff:
        return redirect("home")

    bus = get_object_or_404(
        Bus,
        id=id
    )

    if request.method == "POST":

        bus.current_location = request.POST.get(
            "current_location"
        )

        bus.next_stop = request.POST.get(
            "next_stop"
        )

        bus.eta = request.POST.get(
            "eta"
        )

        bus.status = request.POST.get(
            "status"
        )

        bus.save()

        messages.success(
            request,
            "Bus tracking updated successfully!"
        )

        return redirect(
            "admin_panel"
        )

    return render(
        request,
        "myapp/update_location.html",
        {
            "bus": bus
        }
    )


@login_required
def add_route(request):

    if not request.user.is_staff:
        return redirect('home')

    if request.method == "POST":

        Route.objects.create(

            from_city=request.POST.get(
                "from_city"
            ),

            to_city=request.POST.get(
                "to_city"
            )

        )

        return redirect(
            "admin_panel"
        )

    return render(
        request,
        "myapp/add_route.html"
    )

@login_required
def delete_route(request, id):

    if not request.user.is_staff:
        return redirect("home")

    route = get_object_or_404(
        Route,
        id=id
    )

    route.delete()

    return redirect(
        "admin_panel"
    )

@login_required
def admin_analytics(request):

    if not request.user.is_staff:
        return redirect("home")
    top_users = (

    Booking.objects

    .values(

        'user__username'

    )

    .annotate(

        total_bookings=Count('id'),

        total_spent=Sum('total_fare')

    )

    .order_by(

        '-total_bookings'

    )[:5]

)

    context = {

    "total_users":
        User.objects.count(),

    "total_logins":
        LoginHistory.objects.count(),

    "total_bookings":
        Booking.objects.count(),

    "total_buses":
        Bus.objects.count(),

    "total_routes":
        Route.objects.count(),

    "total_complaints":
        Complaint.objects.count(),

    "total_revenue":
        sum(
            booking.total_fare
            for booking in Booking.objects.all()
        ),

    'top_users': top_users

        }

    

    return render(
        request,
        "myapp/admin_analytics.html",
        context
    )

@login_required
def users_list(request):

    if not request.user.is_staff:
        return redirect("home")

    users = User.objects.all()

    return render(
        request,
        "myapp/users_list.html",
        {
            "users": users
        }
    )


@login_required
def login_history(request):

    if not request.user.is_staff:
        return redirect("home")

    logins = LoginHistory.objects.all().order_by(
        "-login_time"
    )

    return render(
        request,
        "myapp/login_history.html",
        {
            "logins": logins
        }
    )


from django.utils import timezone

def logout_view(request):

    if request.user.is_authenticated:

        login_record = LoginHistory.objects.filter(
            user=request.user,
            logout_time__isnull=True
        ).last()

        if login_record:

            login_record.logout_time = timezone.now()

            login_record.save()

    logout(request)

    return redirect('login')