import sys
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from caka.auth.AuthBackend import AuthBackend


def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')

        # check email
        if User.objects.filter(email=email.lower()).exists():
            messages.warning(request, 'Email are Already Exists !')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username are Already exists !')
            return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')

    return render(request, 'registration/register.html')


def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = AuthBackend.authenticate(request,
                                        email=email,
                                        password=password)
        if user != None:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')

def PROFILE(request):
    return render(request, 'registration/profile.html')

def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        print("====================================\n"
              , username, first_name, last_name, email, password, user_id,repassword,
              "\n===================================")

        if password != None and password != "":
            if password == repassword:
                user.set_password(password)
                messages.success(request, 'Password Successfully changed. ')
            else:
                messages.warning(request, 'Password failed to change or does not same. ')
                return redirect('profile')
        user.save()
        messages.success(request, 'Profile are successfully updated. ')

        return redirect('profile')

def logout_view(request):
    logout(request)
    return redirect('home')


def LOGIN(request):

    return render(request, "registration/login.html")
