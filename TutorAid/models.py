from django.db import models

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    lesson = models.CharField(max_length=10)
    module = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'course'

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    school = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'student'

class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'registration'

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField()
    duration = models.IntegerField()
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'session'

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'attendance'

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    year = models.IntegerField()
    month = models.IntegerField()
    invoiced_at = models.DateField()
    charge = models.IntegerField()
    is_payed = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'invoice'
