from django.urls import path,include
from rest_framework.routers import DefaultRouter

from . import views
from .views import TaskViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet,basename='tasks')
urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('update/<int:task_id>/', views.update_task, name='update_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('',include(router.urls)),
]
