from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    home_view,
    type_account_view,
    register_teacher_view,
    login_view,
    dashboard_teacher_view,
    logout_view
)

urlpatterns = [
    path('', home_view, name='home'),
    path('type-account/', type_account_view, name='type_account'),
    path('register/teacher/', register_teacher_view, name='register_teacher'),
    path('login/', login_view, name='login'),
    path('dashboard/teacher/', dashboard_teacher_view, name='dashboard_teacher'),
    path('logout/', logout_view, name='logout'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)