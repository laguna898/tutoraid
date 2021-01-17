from django import forms
from django.contrib.auth.models import User
from TutorAid import models

#Course
lesson_choices=(('Private', 'Private'), ('Group','Group'))
module_choices=(('IB1', 'IB1'), ('IB2','IB2'), ('SAT', 'SAT'))

class CourseForm(forms.ModelForm):
    class Meta:
        model=models.Course
        lesson=forms.ChoiceField(choices=lesson_choices)
        module=forms.ChoiceField(choices=module_choices)
        fields=['name',lesson,module,'fee_per_hour_per_student']

#Student
class StudentForm(forms.ModelForm):
    class Meta:
        model=models.Student
        fields=['name','contact','school']

#Registration
class RegistrationForm(forms.Form):
    def __init__(self, queryset, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['student'] = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset=queryset)

#Session
class SessionForm(forms.Form):
    duration = forms.IntegerField(help_text="Duration:")

#Attendance
presence_choices=(('Present','Present'),('Absent','Absent'),('Absent by Prior Notice(0%)', 'Absent by Prior Notice(0%)'),('Absent by Late Notice(50%)','Absent by Late Notice(50%)'))
class AttendanceForm(forms.Form):
        status = forms.ChoiceField(choices=presence_choices)

