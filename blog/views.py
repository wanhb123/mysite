from django.shortcuts import render, redirect, reverse
from .models import UserInfo


def index(request):
    return render(request, 'blog/html/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            if username == 'wanhb' and password == '123456':
                return redirect('/blog/login_success/')
            else:
                return render(request, 'blog/html/index.html', {'error': '用户名或密码错误'})
        else:
            return render(request, 'blog/html/index.html', {'error': '用户名或密码为空'})


def login_success(request):
    return render(request, 'blog/html/login_success.html')


def register(request):
    username = request.POST.get('username', '游客')
    password = request.POST.get('password')
    UserInfo.objects.create(username=username, password=password)
    return render(request, 'blog/html/register.html')


def logout(request):
    request.session.flush()   # 清除当前会话，即退出当前用户
    return redirect(reverse('index'))

