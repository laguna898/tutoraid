from django.urls import path

from TutorAid import views

app_name = 'TutorAid'
urlpatterns = [
    path('', views.home_view, name='home'),

    path('courses', views.courses_view, name='courses'),
    path('courses/new', views.course_create_view, name='course_create'),

    path('course/<int:pk>/detail', views.course_detail_view, name='course_detail'),
    path('course/<int:pk>/update', views.course_update_view, name='course_update'),
    path('course/<int:pk>/delete', views.course_delete_view, name='course_delete'),
    path('course/<int:pk>/registration/new', views.registration_create_view, name='registration_create'),
    path('course/<int:pk>/session/new', views.session_create_view, name='session_create'),
    path('session/<int:s_pk>/create-attendance', views.attendance_create_view, name='attendance_create'),
    path('session/<int:s_pk>/update-attendance', views.attendance_update_view, name='attendance_update'),

    path('students', views.students_view, name='students'),
    path('students/new', views.student_create_view, name='student_create'),
    path('student/<int:pk>/detail', views.student_detail_view, name='student_detail'),
    path('student/<int:pk>/update', views.student_update_view, name='student_update'),
    path('student/<int:pk>/delete', views.student_delete_view, name='student_delete'),

    path('sessions', views.sessions_view, name='sessions'),

    path('invoices', views.invoices_view, name='invoices'),
    path('invoices/create-monthly-invoices', views.invoices_create_view, name='invoices_create'),
    path('invoice/<int:pk>/approve', views.invoice_approve_view, name='invoice_approve'),

]