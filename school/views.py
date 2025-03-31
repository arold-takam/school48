from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, TeacherRegistrationForm
from .models import CustomUser, Teacher


def home_view(request):
    """ Page d'accueil pour les visiteurs non authentifiés """
    return render(request, 'school/index.html')


def type_account_view(request):
    """ Choix du type de compte """
    if request.user.is_authenticated:
        return redirect('dashboard_teacher')  # Adapté pour enseignant pour l'instant
    return render(request, 'school/typeAccount.html')


def register_teacher_view(request):
    """ Inscription enseignant """
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, request.FILES)
        teacher_form = TeacherRegistrationForm(request.POST)

        if user_form.is_valid() and teacher_form.is_valid():
            # Création de l'utilisateur avec rôle teacher
            user = user_form.save(commit=False)
            user.role = 'teacher'
            user.save()

            # Création du profil enseignant
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()

            messages.success(request, 'Inscription réussie! Veuillez vous connecter.')
            return redirect('login')

    else:
        user_form = CustomUserCreationForm()
        teacher_form = TeacherRegistrationForm()

    return render(request, 'school/signUpTeacher.html', {
        'user_form': user_form,
        'teacher_form': teacher_form
    })


def login_view(request):
    """ Connexion avec vérification du rôle """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.role == 'teacher':
                login(request, user)
                return redirect('dashboard_teacher')
            else:
                messages.error(request,
                               f"Votre rôle est {user.get_role_display()}. Veuillez choisir le bon formulaire.")
                return redirect('type_account')
        else:
            messages.error(request, 'Identifiants incorrects')

    return render(request, 'school/login.html')


@login_required
def dashboard_teacher_view(request):
    """ Dashboard enseignant """
    if request.user.role != 'teacher':
        return redirect('type_account')

    try:
        teacher_profile = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return redirect('logout')

    return render(request, 'school/dashboardTeacher.html', {
        'teacher': teacher_profile
    })


def logout_view(request):
    """ Déconnexion """
    logout(request)
    return redirect('home')