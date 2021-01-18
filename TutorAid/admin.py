from django.contrib import admin

from .models import Course, Registration, Session, Attendance, Invoice
from .models import Student

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Registration)
admin.site.register(Session)
admin.site.register(Attendance)
admin.site.register(Invoice)
