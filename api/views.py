from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from .models import Task
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import IdSerializer, TaskAddSerializer,UserAddSerializer



class UserView(APIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()


    def get(self, request):
        user_id = request.query_params.get('id')
        try:
            if user_id is not None and user_id != '':
                serializer = IdSerializer(data=request.query_params)
                if not serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': serializer.errors
                    }, status=400)
                data = serializer.data
                user = User.objects.filter(id=data['id']).first()
                if user is None:
                    return Response({
                        'success': False,
                        'message': 'User not found'
                    }, status=400)
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
                return Response({
                    'success': True,
                    'data': user_data
                }, status=200)
            else:
                if request.user.is_superuser:
                    users = list(User.objects.all().values())
                else:
                    users = list(User.objects.filter(id=request.user.id).values())
                
                return Response({
                    'success': True,
                    'data': users
                }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Getting user failed'
            }, status=400)


    def post(self, request):
        try:
            serializer = UserAddSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': serializer.errors
                }, status=400)
            data = serializer.validated_data
            user = User.objects.filter(username=data['username'],
                                       email=data['email']).first()
            if user:
                return Response({
                    'success': False,
                    'message': 'User already exists'
                }, status=400)
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                # ... diğer özellikler
            }
            return Response({
                'success': True,
                'message': 'User added',
                'data': user_data
            }, status=200)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Adding user is failed'
            }, status=400)

    def delete(self, request):
        try:
            serializer = IdSerializer(data=request.query_params)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=400)
            data = serializer.validated_data
            user = User.objects.filter(id=data['id']).first()
            if user is None:
                return Response({
                    'success': False,
                    'message': 'User not found'
                }, status=400)
            user.delete()
            return Response({
                'success': True,
                'message': 'User deleted',
                'data': data['id']
            }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Deleting user is failed'
            }, status=400)




class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    

    def get(self, request):
        task_id = request.query_params.get('id')
        try:
            if task_id is not None and task_id != '':
                serializer = IdSerializer(data=request.query_params)
                if not serializer.is_valid():
                    return Response({
                        'success': False,
                        'message': serializer.errors
                    }, status=400)
                data = serializer.data
                task = Task.objects.filter(id=data['id'], user=request.user).first()
                if task is None:
                    return Response({
                        'success': False,
                        'message': 'Task not found'
                    }, status=400)
                task_data = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'created_at': task.created_at,
                    # ... diğer özellikler
                }
                return Response({
                    'success': True,
                    'data': task_data
                }, status=200)
            else:
                tasks = Task.objects.filter(user=request.user).values()
                return Response({
                    'success': True,
                    'data': list(tasks)
                }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Getting tasks failed'
            }, status=400)

    def post(self, request):
        try:
            serializer = TaskAddSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': serializer.errors
                }, status=400)
            data = serializer.validated_data
            task = Task.objects.create(user=request.user, title=data['title'], description=data['description'])
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at,
                # ... diğer özellikler
            }
            return Response({
                'success': True,
                'message': 'Task added',
                'data': task_data
            }, status=200)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Adding task failed'
            }, status=400)

    def delete(self, request):
        try:
            serializer = IdSerializer(data=request.query_params)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Task not found'
                }, status=400)
            data = serializer.validated_data
            task = Task.objects.filter(id=data['id'], user=request.user).first()
            if task is None:
                return Response({
                    'success': False,
                    'message': 'Task not found'
                }, status=400)
            task.delete()
            return Response({
                'success': True,
                'message': 'Task deleted',
                'data': data['id']
            }, status=200)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Deleting task failed'
            }, status=400)
    
    def put(self, request):
        try:
            print(f"Request Data: {request.data}")
            serializer = IdSerializer(data=request.data)
            if not serializer.is_valid():
                return Response({
                    'success': False,
                    'message': 'Invalid ID'
                }, status=400)
        
            data = serializer.validated_data
            task = Task.objects.filter(id=data['id'], user=request.user).first()
            if task is None:
                return Response({
                    'success': False,
                    'message': 'Task not found'
                }, status=400)

            update_serializer = TaskAddSerializer(instance=task,data=request.data, partial=True)
            if not update_serializer.is_valid():
                return Response({
                    'success': False,
                    'message': update_serializer.errors
                }, status=400)

            update_data = update_serializer.validated_data
            task.title = update_data.get('title', task.title)
            task.description = update_data.get('description', task.description)
            task.save()

            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'created_at': task.created_at,
                # ... diğer özellikler
            }
            return Response({
                'success': True,
                'message': 'Task updated',
                'data': task_data
            }, status=200)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Updating task failed'
            }, status=400)
