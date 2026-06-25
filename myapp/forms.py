from django import forms
from .models import Student
from django.contrib.auth.models import User

class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'age', 'rollno', 'dept']


class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username', 'email', 'password']
