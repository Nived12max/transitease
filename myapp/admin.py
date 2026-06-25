from django.contrib import admin
from .models import Student
from .models import Booking

# Register your models here.
admin.site.register(Student)
from .models import emp
admin.site.register(emp)
admin.site.register(Booking)