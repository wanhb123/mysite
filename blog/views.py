from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, redirect
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
    print(search_result)
    event_list = Event.objects.filter(title_name__contains=search_result)
    print(event_list)
    return render(request, "blog/html/event_manage.html", {"user": username, "events": event_list})


@login_required
def search_phone(request):
    username = request.session.get('user', '')
    phone = request.GET.get('phone')
    if not phone:
        render(request, 'blog/html/guest_manage.html', {'user': username, 'msg': '手机号不存在'})
    else:
        guest_list = Guest.objects.get(phone__contains=phone)
        page = request.GET.get('page')
        paginator = Paginator(guest_list, 5)
        try:
            content = paginator.page(page)
        except EmptyPage:
            content = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            content = paginator.page(1)
        return render(request, 'blog/html/guest_manage.html', {'user': username, 'guests': content})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '游客')
        password = request.POST.get('password')
        pwd = make_password(password)
        UserInfo.objects.create(username=username, password=pwd)
        return redirect('/blog/index/')
    return render(request, 'blog/html/register.html')


@login_required
def add_event1(request):
    return render(request, 'blog/html/add_event.html')


@login_required
def add_event(request):
    eid = request.POST.get('eid', '')  # 发布会
    name = request.POST.get('title_name', '')  # 发布会标题
    limit = request.POST.get('limit', '')  # 限制人数
    status = request.POST.get('status', '')  # 状态
    address = request.POST.get('address', '')  # 地址
    start_time = request.POST.get('start_time', '')  # 发布会时间
    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})
    if status == '':
        status = 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError:
        error = 'start_time format error. It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'add event success'})


def logout(request):
    # 清除当前会话，退出当前用户
    auth.logout(request)
    return redirect('/blog/index/')

