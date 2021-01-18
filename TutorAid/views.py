from itertools import groupby

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
            return HttpResponseRedirect(reverse('TutorAid:courses'))
    return render(request, 'TutorAid/course_create.html', {'form': form})


def course_detail_view(request, pk):
    course = Course.objects.get(id=pk)
    registrations = course.registration_set.select_related('student')
    registered_students = [registration.student for registration in registrations]
    course_sessions = Session.objects.all().filter(course_id=pk)

    return render(request, 'TutorAid/course_detail.html',
                  {'course': course, 'registrations': registrations, 'course_sessions': course_sessions})


def course_update_view(request, pk):
    course = Course.objects.get(id=pk)
    form = forms.CourseForm(instance=course)
    if request.method == 'POST':
        form = forms.CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect(reverse('TutorAid:course_detail', kwargs={'pk': pk}), )
    return render(request, 'TutorAid/course_update.html', {'form': form, 'course': course})


def course_delete_view(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect(reverse('TutorAid:courses'))


def registration_create_view(request, pk):
    course = Course.objects.get(id=pk)
    registered_students = course.registration_set.values('student_id').all()
    registrationForm = forms.RegistrationForm(Student.objects.all().exclude(id__in=registered_students))
    if request.method == 'POST':
        form = forms.RegistrationForm(Student.objects, request.POST)
        if form.is_valid():
            Students = form.cleaned_data.get('students')
            for i in range(len(Students)):
                RegistrationModel = Registration()
                RegistrationModel.course_id = pk
                RegistrationModel.student_id = Students[i].id
                RegistrationModel.save()
            return HttpResponseRedirect(reverse('TutorAid:course_detail', args=[pk]))
    return render(request, 'TutorAid/registration_create.html',
                  {'form': registrationForm, 'course': course, 'registered_students': registered_students})

def registration_delete_view(request, pk, registration_id):
    registration = Registration.objects.get(id=registration_id)
    registration.delete()
    return redirect(reverse('TutorAid:course_detail', args=[pk]))

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
            return redirect(reverse('TutorAid:attendance_create', args=[SessionModel.id]))
    return render(request, 'TutorAid/session_create.html',
                  {'form': form, 'course': course, 'course_sessions': course_sessions})


def attendance_create_view(request, session_id):
    session = Session.objects.get(id=session_id)
    students = [registration.student for registration in session.course.registration_set.order_by('id')]
    initial_values = [{'status': 'Present'} for _ in students]
    formset = forms.AttendanceFormSet(initial=initial_values)
    if request.method == 'POST':
        formset = forms.AttendanceFormSet(request.POST, initial=initial_values)
        if formset.is_valid():
            for student, form in zip(students, formset):
                AttendanceModel = Attendance()
                AttendanceModel.session = session
                AttendanceModel.student = student
                AttendanceModel.status = form.cleaned_data['status']
                AttendanceModel.save()
        return redirect(reverse('TutorAid:course_detail', args=[session.course.get_id]))
    return render(request, 'TutorAid/attendance_create.html',
                  {'attendance_data': zip(students, formset), 'formset': formset})


def attendance_update_view(request, session_id):
    session = Session.objects.get(id=session_id)
    attendances = session.attendance_set.order_by('id')
    students = list(map(lambda x: x.student, attendances))
    initial_values = [{'status': attendance.status} for attendance in attendances]
    formset = forms.AttendanceFormSet(initial=initial_values)
    if request.method == 'POST':
        formset = forms.AttendanceFormSet(request.POST, initial=initial_values)
        if formset.is_valid():
            for attendance, form in zip(attendances, formset):
                attendance.status = form.cleaned_data['status']
                attendance.save()
        return redirect(reverse('TutorAid:course_detail', args=[session.course.get_id]))
    return render(request, 'TutorAid/attendance_create.html',
                  {'attendance_data': zip(students, formset), 'formset': formset})


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
            return HttpResponseRedirect(reverse('TutorAid:students'))
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
        form = forms.StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect(reverse('TutorAid:student_detail', kwargs={'pk': pk}))
    return render(request, 'TutorAid/student_update.html', {'form': form, 'student': student})


def student_delete_view(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect(reverse('TutorAid:students'))

def sessions_view(request):
    sessions = Session.objects.all()
    return render(request, 'TutorAid/sessions.html', {'sessions': sessions})


def invoices_view(request):
    invoices = Invoice.objects.select_related('student').order_by('-year', '-month')
    return render(request, 'TutorAid/invoices.html', {'invoices': invoices})


def invoices_create_view(request):
    # if invoices of previous month already exist, cannot create a new one
    # can only create invoices of previous month from the first day of current month

    today = datetime.today()
    current_month = today.replace(month=today.month + 1, day=1, hour=0, minute=0, microsecond=0)
    last_day_of_prev_month = current_month - timedelta(days=1)
    start_day_of_prev_month = current_month - timedelta(days=last_day_of_prev_month.day)
    atts = Attendance\
        .objects\
        .select_related('session__course', 'student')\
        .filter(created_at__gte=start_day_of_prev_month, created_at__lt=last_day_of_prev_month)\
        .order_by('student__name')
    atts_by_student = groupby(atts, lambda att: att.student)

    for student, atts in atts_by_student:

        def calc_att_rate(att: Attendance):
            if att.status == 'Absent by Prior Notice(0%)':
                return 0
            if att.status == 'Absent by Late Notice(50%)':
                return 0.5
            return 1

        fee = sum(map(lambda att: calc_att_rate(att) * att.session.duration * att.session.course.fee_per_hour_per_student, atts))

        invoice = Invoice()
        invoice.student = student
        invoice.charge = fee
        invoice.year = last_day_of_prev_month.year
        invoice.month = last_day_of_prev_month.month
        invoice.save()

    return redirect(reverse('TutorAid:invoices'))


def invoice_approve_view(request, pk):
    invoice = Invoice.objects.get(id=pk)
    invoice.is_payed = True
    invoice.save()
    return redirect('TutorAid/invoice_approve.html')
