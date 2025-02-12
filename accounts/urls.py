from django.urls import path

from . import views
from .views import email_dogrulama, verify_email
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.login_view, name='home'),
    path('register/',views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/',views.task_list, name='task_list'),
    path('profil/',views.profile, name='profil'),
    path('verify-email-request/', email_dogrulama, name='verify_email_request'),
    path('email-dogrula/<str:token>/', verify_email, name='verify_email'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),

]
