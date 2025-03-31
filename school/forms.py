from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Teacher, Student


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'gender', 'phone', 'photo']


class TeacherRegistrationForm(forms.ModelForm):
    hiring_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date d'embauche"
    )

    class Meta:
        model = Teacher
        fields = ['diploma', 'specialization', 'hiring_date']

class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['matricule', 'birthday', 'class_level', 'parent']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
        }