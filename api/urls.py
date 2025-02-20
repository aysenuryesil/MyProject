from django.urls import path
from .views import *

urlpatterns = [
    path('register/', UserView.as_view(), name='register'),
    path('tasks/',TaskView.as_view(),name='tasks'),
  ]