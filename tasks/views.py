from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Task
from django.shortcuts import get_object_or_404

from .serializers import TaskSerializer


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Task.objects.create(user=request.user,title=title, description=description)
        return redirect('task_list')
    return render(request, "create_task.html")
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})
@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', task.description)
        task.save()
        return redirect('task_list')
    return render(request, 'update_task.html', {'task': task})
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'delete_task.html', {'task': task})

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

