from django.db.models import QuerySet
from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseRedirect

from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import Group

from django.db.models import Sum, F, Value

from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect

from .models import Course, Student, Registration, Session, Attendance, Invoice
from . import forms
from datetime import datetime, timedelta


def home_view(request):
    return render(request, 'TutorAid/home.html')


def courses_view(request):
    courses = Course.objects.all()
    return render(request, 'TutorAid/courses.html', {'courses': courses})


def course_create_view(request):
    form = forms.CourseForm()
    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            course.save()
            return HttpResponseRedirect('courses')
    return render(request, 'TutorAid/course_create.html', {'form': form})


def course_detail_view(request, pk):
    course = Course.objects.get(id=pk)
    registrations = Registration.objects.all().filter(course_id=pk).values("student_id")
    registered_students = Student.objects.all().filter(id__in=registrations)
    course_sessions = Session.objects.all().filter(course_id=pk)

    return render(request, 'TutorAid/course_detail.html',
                  {'course': course, 'registered_students': registered_students, 'course_sessions': course_sessions})


def course_update_view(request, pk):
    course = Course.objects.get(id=pk)
    form = forms.CourseForm(instance=course)
    if request.method == 'POST':
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            course.save()
            return redirect('course_detail', pk)
    return render(request, 'TutorAid/course_update.html', {'form': form, 'course': course})


def course_delete_view(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect('TutorAid/courses.html')


def registration_create_view(request, course_id):
    course = Course.objects.get(id=course_id)
    registered_students = Registration.objects.get(course_id=course_id)
    registrationForm = forms.RegistrationForm()
    if request.method == 'POST':
        form = forms.RegistrationForm(Student.objects.all().filter(id=registered_students.student_id), request.POST)
        if form.is_valid():
            Students = form.cleaned_data.get('students')
            for i in range(len(Students)):
                RegistrationModel = Registration()
                RegistrationModel.course_id = course_id
                RegistrationModel.student_id = Students[i]
                RegistrationModel.save()
            return HttpResponseRedirect('course_detail')
    return render(request, 'TutorAid/registration_create.html',
                  {'form': registrationForm, 'course': course, 'registered_students': registered_students})


def session_create_view(request, course_id):
    course = Course.objects.get(id=course_id)
    course_sessions = Session.objects.all().filter(course_id=course_id)
    form = forms.SessionForm()
    if request.method == 'POST':
        form = forms.SessionForm(request.POST)
        if form.is_valid():
            SessionModel = Session()
            SessionModel.course_id = course_id
            SessionModel.duration = form.cleaned_data.get('duration')
            SessionModel.save()
            return redirect('attendance_create', SessionModel.id)
    return render(request, 'TutorAid/session_create.html',
                  {'form': form, 'course': course, 'course_sessions': course_sessions})


def attendance_create_view(request, session_id):
    session = Session.objects.get(id=session_id)
    course = Course.objects.get(id=session.course_id)
    registered_students = Registration.objects.all().filter(course_id=course.id)
    students = Student.objects.all().filter(id=registered_students.student_id)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('status')
            for i in range(len(Attendances)):
                AttendanceModel = Attendance()
                AttendanceModel.session_id = session_id
                AttendanceModel.student_id = students[i]
                AttendanceModel.status = Attendances[i]
                AttendanceModel.save()
            return redirect('course_detail', course.id)
    return render(request, 'TutorAid/attendance_create.html', {'students': students, 'form': aform})


def attendance_update_view(request, session_id):
    attendances = Attendance.objects.all().filter(session_id=session_id)
    session = Session.objects.get(id=session_id)
    course = Course.objects.get(id=session.course_id)
    registered_students = Registration.objects.all().filter(course_id=course.id)
    students = Student.objects.all().filter(id=registered_students.student_id)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('status')
            for i in range(len(Attendances)):
                AttendanceModel = Attendance()
                AttendanceModel.session_id = session_id
                AttendanceModel.student_id = students[i]
                AttendanceModel.status = Attendances[i]
                AttendanceModel.save()
            return redirect('course_detail', course.id)
    return render(request, 'TutorAid/attendance_update.html', {'attendances': attendances, 'form': aform})


def students_view(request):
    students = Student.objects.all()
    return render(request, 'TutorAid/students.html', {'students': students})


def student_create_view(request):
    form = forms.StudentForm()
    if request.method == 'POST':
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            student.save()
            return HttpResponseRedirect('students')
    return render(request, 'TutorAid/student_create.html', {'form': form})


def student_detail_view(request, pk):
    student = Student.objects.get(id=pk)
    registrations = Registration.objects.all().filter(student_id=pk).values("course_id")
    registered_courses = Course.objects.all().filter(id__in=registrations)
    invoices = Invoice.objects.all().filter(student_id=pk)

    return render(request, 'TutorAid/student_detail.html',
                  {'student': student, 'registered_courses': registered_courses, 'invoices': invoices})


def student_update_view(request, pk):
    student = Student.objects.get(id=pk)
    form = forms.StudentForm(instance=student)
    if request.method == 'POST':
        form = forms.StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            student.save()
            return redirect('student_detail', pk)
    return render(request, 'TutorAid/student_update.html', {'form': form, 'student': student})


def student_delete_view(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect('TutorAid/students.html')


def sessions_view(request):
    sessions = Student.objects.all()
    return render(request, 'TutorAid/sessions.html', {'sessions': sessions})


def invoices_view(request):
    invoices = Invoice.objects.select_related('student').order_by('-year', '-month')
    return render(request, 'TutorAid/invoices.html', {'invoices': invoices})


def invoices_create_view(request):
    # if invoices of previous month already exist, cannot create a new one
    # can only create invoices of previous month from the first day of current month

    last_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=1)
    start_day_of_prev_month = datetime.today().replace(day=1) - timedelta(days=last_day_of_prev_month.day)

    feeCalculation = Student.objects.select_related('attendance').select_related('session').select_related(
        'course').filter(attendance__session_id__created_at__gte=start_day_of_prev_month,
                         attendance__session_id__created_at__lte=last_day_of_prev_month).values('name').annotate(fee=Sum(F('fee_per_hour_per_student')*F('duration')*F('status')))

    #invoice.save()
    return redirect('TutorAid/invoices.html')


def invoice_approve_view(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoice.is_payed = True
    invoice.save()
    return redirect('TutorAid/invoice_approve.html')
