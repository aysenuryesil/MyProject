from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserView.as_view(), name='register'),
    path('tasks/',TaskView.as_view(),name='tasks'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('emailverification/',EmailVerificationView.as_view(),name='emailverification'),
    path('verifyemail/', VerifyEmailView.as_view(), name='verifyemail'),
    path('updatepassword/<int:id>/', ChangePassword.as_view(), name='updatepassword'),

  ]