from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('teacher', 'Enseignant'),
        ('parent', 'Parent'),
        ('student', 'Étudiant'),
    )

    GENDER_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )

    # Suppression des champs inutiles
    first_name = None
    last_name = None

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    photo = models.ImageField(
        upload_to='profile_photos/',
        validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
        blank=True,
        null=True
    )
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    last_connexion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Teacher(models.Model):
    DIPLOMA_CHOICES = (
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('phd', 'Doctorat'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    diploma = models.CharField(max_length=10, choices=DIPLOMA_CHOICES)
    specialization = models.CharField(max_length=100)
    hiring_date = models.DateField()
    classes_taught = models.ManyToManyField('Class')

    def __str__(self):
        return f"Enseignant: {self.user.username}"


class Parent(models.Model):
    PARENT_TYPE_CHOICES = (
        ('biologic', 'Biologique'),
        ('adoptiv', 'Adoptif'),
        ('tutor', 'Tuteur'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    parent_type = models.CharField(max_length=10, choices=PARENT_TYPE_CHOICES)
    spouse = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Parent: {self.user.username}"


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    matricule = models.CharField(max_length=20, unique=True)
    birthday = models.DateField()
    class_level = models.ForeignKey('Class', on_delete=models.SET_NULL, null=True)
    inscription_date = models.DateField(auto_now_add=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)

    def __str__(self):
        return f"Étudiant: {self.user.username}"


class Class(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name