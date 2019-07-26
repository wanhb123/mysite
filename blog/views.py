from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, reverse
from .models import UserInfo, Event, Guest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'blog/html/index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username == '' or password == '':
            return render(request, 'blog/html/index.html', {'error': '用户名或密码为空'})
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            request.session['user'] = username
            return redirect('/blog/event_manage/')

        else:
            return render(request, 'blog/html/index.html', {'error': '用户名或密码错误'})
    return render(request, 'blog/html/index.html')


@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', 'xxx')
    return render(request, 'blog/html/event_manage.html', {'user': username, 'events': event_list})


@login_required
def guest_manage(request):
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 5)
    username = request.session.get('user', 'xxx')
    page = request.GET.get('page')
    try:
        content = paginator.page(page)
    except EmptyPage:
        content = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        content = paginator.page(1)
    return render(request, 'blog/html/guest_manage.html', {'user': username, 'guests': content})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_result = request.GET.get("name", "")
    try:
        event_list = Event.objects.filter(title_name__contains=search_result)
    except Exception as e:
        return render(request, "blog/html/event_manage.html", {'errMsg': e})
    finally:
        return render(request, "blog/html/event_manage.html", {"user": username, "events": event_list})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '游客')
        password = request.POST.get('password')
        pwd = make_password(password)
        UserInfo.objects.create(username=username, password=pwd)
        return redirect('/blog/index/')
    return render(request, 'blog/html/register.html')


def error(request):
    return render(request, 'blog/html/404.html')


def logout(request):
    # 清除当前会话，退出当前用户
    auth.logout(request)
    return redirect('/blog/index/')

