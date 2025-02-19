from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserView.as_view(), name='login'),
  ]