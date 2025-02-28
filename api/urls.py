from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserView.as_view(), name='registerV'),
    path('tasks/',TaskView.as_view(),name='tasksV'),
    path('logout/',LogoutView.as_view(),name='logoutV'),
    path('profile/',ProfileView.as_view(),name='profileV'),
    path('emailverification/',EmailVerificationView.as_view(),name='emailverificationV'),
    path('verifyemail/', VerifyEmailView.as_view(), name='verifyemailV'),
    path('updatepassword/<int:id>/', ChangePassword.as_view(), name='updatepasswordV'),

  ]