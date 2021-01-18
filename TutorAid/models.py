from django.db import models

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    lesson = models.CharField(max_length=10)
    module = models.CharField(max_length=10)
    fee_per_hour_per_student = models.IntegerField()

    def __str__(self):
        return self.name + "|" + self.lesson + "|" + self.module
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.name

    class Meta:
        db_table = 'course'

class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    contact = models.CharField(max_length=10)
    school = models.CharField(max_length=10)

    def __str__(self):
        return self.name + "|" + self.school + "|" + self.contact
    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.name

    class Meta:
        db_table = 'student'

class Registration(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'registration'

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    @property
    def get_id(self):
        return self.id
    @property
    def get_name(self):
        return self.course_id.__str__()

    class Meta:
        db_table = 'session'

class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=30)

    @property
    def get_session(self):
        return self.session_id.get_name
    @property
    def get_student(self):
        return self.student_id.__str__()

    class Meta:
        db_table = 'attendance'

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    invoiced_at = models.DateField(auto_now_add=True)
    charge = models.FloatField()
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return "{} - {}/{}|{}".format(self.student, self.year, self.month, self.charge)

    class Meta:
        db_table = 'invoice'
