from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect, reverse
from .models import UserInfo


def index(request):
    return render(request, 'blog/html/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            request.session['user'] = username
            return redirect('/blog/login_success/')

        else:
            return render(request, 'blog/html/index.html', {'error': '用户名或密码错误'})


@login_required
def login_success(request):
    username = request.session.get('user', 'xxx')
    return render(request, 'blog/html/login_success.html', {'msg': username})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '游客')
        password = request.POST.get('password')
        pwd = make_password(password)
        UserInfo.objects.create(username=username, password=pwd)
        return redirect('/blog/index/')
    return render(request, 'blog/html/register.html')


def logout(request):
    # 清除当前会话，退出当前用户
    auth.logout(request)
    return redirect(reverse('index'))

