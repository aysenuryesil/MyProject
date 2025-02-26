from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers
from .models import Task
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import IdSerializer, TaskAddSerializer,UserAddSerializer,ChangePasswordSerializer
from django.contrib.auth import logout
from rest_framework import status
from .models import Profile
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.generics import UpdateAPIView

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
                    users = list(User
                    .objects.all().values())
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
    




    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({
                'success': True,
                'message': 'Çıkış başarılı'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Exception: {e}")
            return Response({
                'success': False,
                'message': 'Çıkış işlemi başarısız oldu'
            }, status=status.HTTP_400_BAD_REQUEST)

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
            serializer = IdSerializer(data=request.query_params)
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



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        user_data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'is_verified': user_profile.is_verified,
        }
        return Response(user_data)

    def put(self, request):
        user = request.user
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.email = request.data.get("email", user.email)
        user.save()
        return Response({"message": "Profil başarıyla güncellendi."}, status=status.HTTP_200_OK)

class EmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = get_random_string(length=32)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.email_token = token
        profile.save()

        dogrulama_linki = request.build_absolute_uri(f"/api/verifyemail/{token}/")

        send_mail(
            'E-Posta Doğrulama',
            f"Lütfen e-posta adresinizi doğrulamak için şu linke tıklayın: {dogrulama_linki}",
            'admin@seninsiten.com',
            [request.user.email],
            fail_silently=False,
        )

        return Response({"message": "E-Posta doğrulama bağlantısı gönderildi!"}, status=status.HTTP_200_OK)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            profile = Profile.objects.get(email_token=token)
            if profile.is_verified:
                return Response({"message": "E-posta zaten doğrulanmış!"}, status=status.HTTP_200_OK)
            profile.is_verified = True
            profile.email_token = ''
            profile.save()
            return Response({"message": "E-posta başarıyla doğrulandı!"}, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({"error": "Geçersiz doğrulama linki."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @method_decorator(csrf_exempt)
    def put(self, request, id):
        try:
            password1 = request.data.get('password1')
            password2 = request.data.get('password2')

            if not password1 or not password2:
                return Response({'error': 'password fields cannot be empty'}, status=400)

            obj = get_user_model().objects.get(pk=id)
            if not obj.check_password(raw_password=password1):
                return Response({'error': 'password not match'}, status=400)

            obj.set_password(password2)
            obj.save()

            return Response({'success': 'password changed successfully'}, status=200)

        except Exception as e:
            print(f"Exception: {e}")
            return Response({'error': f'password change failed: {e}'}, status=500)