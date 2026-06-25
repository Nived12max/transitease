"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sfd',views.sample),
    path('ss',views.demo),
    path('aa',views.demo1),
    path('bb',views.demo2),
    path('ddd',views.demo3),
    path('s', views.student_list),
    path('empp',views.emp1),
    path('add', views.student_form, name='studentform'),
    path('show', views.show_students, name='showstudents'),
    path('edit/<int:id>', views.edit_student),
    path('delete/<int:id>', views.delete_student),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('', views.home, name='home'),
    path('buses/', views.bus_list, name='bus_list'),
    path('seats/', views.seat_selection, name='seat_selection'),
    path('passenger/', views.passenger_details, name='passenger'),
    path('summary/', views.booking_summary, name='summary'),
    path('support/', views.support, name='support'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('support/',views.support,name='support'),
    path('my-bookings/',views.my_bookings,name='my_bookings'),
    path('ticket/<int:id>/',views.ticket,name='ticket'),
    path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path(
    'download-ticket/<int:id>/',
    views.download_ticket,
    name='download_ticket'
),
    path(
    'pickup-drop/',
    views.pickup_drop,
    name='pickup_drop'
),
    path(
    'verify-ticket/',
    views.verify_ticket,
    name='verify_ticket'
),
    path(
    'admin-panel/',
    views.admin_panel,
    name='admin_panel'
),

    path('add-bus/', views.add_bus, name='add_bus'),
    path('edit-bus/<int:id>/', views.edit_bus, name='edit_bus'),
    path(
    'delete-bus/<int:id>/',
    views.delete_bus,
    name='delete_bus'
),
    path(
        'complaints/',
        views.complaints,
        name='complaints'
    ),

    path(
        'notifications/',
        views.notifications,
        name='notifications'
    ),

    path(
        'admin-complaints/',
        views.admin_complaints,
        name='admin_complaints'
    ),

    path(
        'reply-complaint/<int:id>/',
        views.reply_complaint,
        name='reply_complaint'
    ),
    path(
    'track-bus/<int:id>/',
    views.track_bus,
    name='track_bus'
),
    path(
    'update-location/<int:id>/',
    views.update_location,
    name='update_location'
),
 

    path(
    'add-route/',
    views.add_route,
    name='add_route'
),
    path(
    'delete-route/<int:id>/',
    views.delete_route,
    name='delete_route'
),



path(
    'admin-analytics/',
    views.admin_analytics,
    name='admin_analytics'
),


path(
    'users-list/',
    views.users_list,
    name='users_list'
),

path(
    'login-history/',
    views.login_history,
    name='login_history'
),



]

