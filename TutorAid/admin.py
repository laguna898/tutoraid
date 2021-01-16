from django.contrib import admin

from .models import Course
from .models import Student

admin.site.register(Course)
admin.site.register(Student)

