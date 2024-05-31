from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from datetime import datetime
from .models import *
from core.views import *

# Create your views here.

def moderator_reg(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        token = request.POST.get('token')

        a_token = Token.objects.get(id=1)

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username already taken')
            
        else:
            if password == confirm_password:
                if token == a_token.token:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    moderator = Moderator(user=user, token=a_token.token, created_at=datetime.now())
                    moderator.save()
                    return redirect(moderator_login)
            
                else:
                    messages.info(request, "Please get a valid token")     
            
            else:
                messages.info(request, "password does not match")
                
    return render(request, 'accounts/moderator_reg.html')



def moderator_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            our_user = User.objects.get(username=username)
            if Moderator.objects.filter(user=our_user).exists():
                auth.login(request, user)
                return redirect(moderator_dashboard)
            else:
                messages.info(request, 'You do not have Admin priviledge')
        else:
            messages.info(request, 'incorrect username or password')
        
    return render(request, 'accounts/moderator_login.html')

def moderator_logout(request):
    auth.logout(request)
    return redirect(index)

def visitor_reg(request):
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "username already taken")
    
        else:
            if password == confirm_password:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                visitor = Visitor(user=user, created_at=datetime.now(), is_authorized=False)
                visitor.save()
                messages.info(request, 'user created successfully, wait for your account to be authorizedd')
                return redirect(visitor_login)   
            else:
                messages.info(request, "password does not match")

    return render(request, 'accounts/visitor_reg.html')

def visitor_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            our_user = User.objects.get(username=username)
            visitor = Visitor.objects.get(user=our_user)
            if visitor.is_authorized:
                auth.login(request, user)
                return redirect(visitor_dashboard)
            else:
                messages.info(request, 'you are not authorized')
        else:
            messages.info(request, 'incorrect username or password')

    return render(request, 'accounts/visitor_login.html')

def visitor_logout(request):
    auth.logout(request)
    return redirect(index)