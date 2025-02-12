from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from pyexpat.errors import messages
from django.contrib import messages
from django.core.mail import send_mail
from django.views import View


from .models import Profile
from tasks.models import Task



def login_view(request):
    if request.user.is_authenticated:
        return redirect('task_list')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'!!!Geçersiz Giriş Bilgileri!!!')

    else:
        form = AuthenticationForm()
    return render (request, 'login.html',{'form':form})



@login_required
def task_list(request):
    tasks=Task.objects.filter(user=request.user)
    return render(request,'task_list.html',{'tasks':tasks})

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render (request, 'home.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request,'Şifreler uyuşmuyor!!!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Bu kullanıcı adı zaten alınmış!!!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request,"Bu e-posta adresi zaten kullanılıyor!!!")
            return redirect ('register')

        if password1 == password2:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password1
            )
            user.save()
            messages.success(request,"Başarıyla kayıt oldunuz! Giriş yapabilirsiniz.")
            return redirect("login")

    return render(request, "register.html")

@login_required
def profile(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': user_profile})


@login_required
def email_dogrulama(request):
    if request.method == "POST":
        token = get_random_string(length=32)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.email_token = token
        profile.save()
        print(profile.email_token)

        dogrulama_linki = request.build_absolute_uri(f"/email-dogrula/{token}/")

        send_mail(
            'E-Posta Doğrulama',
            f"Lütfen e-posta adresinizi doğrulamak için şu linke tıklayın: {dogrulama_linki}",
            'admin@seninsiten.com',
            [request.user.email],
            fail_silently=False,
        )

        messages.success(request, "E-Posta doğrulama bağlantısı gönderildi!")
        return redirect('profil')


def verify_email(request, token):
    try:
        profile = Profile.objects.get(email_token=token)
        profile.is_verified = True
        profile.email_token = ''
        profile.save()
        messages.success(request, "E-posta başarıyla doğrulandı!")
    except Profile.DoesNotExist:
        messages.error(request, "Geçersiz doğrulama linki.")
    return redirect('profil')


@login_required
def update_profile(request):
    if request.method == "POST":
        user=request.user
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.save()
        messages.success(request,"Profil başarıyla güncellendi.")
        return redirect('profil')
    return render(request,'profile.html')



