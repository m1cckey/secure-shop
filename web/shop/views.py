from django.shortcuts import render
from django.db import connection
from .security import hash_pas, check_password, signature, verify_signature
from .models import User
from django.shortcuts import redirect
from .authlog import auth_logger
import time
from django.http import HttpResponse
import json

js_path = '/Users/lenar/Desktop/secure-shop/secrets/config.json'
with open(js_path, 'r', encoding='utf-8') as f:
  data = json.load(f)
  Cookie_key = data.get('Cookie_key')

def render_page(request, template, context=None):
    return render(request, template, context or {})

def index(request):
    return render_page(request, 'index.html')

def login(request):
    response = HttpResponse()
    if request.method == 'GET':
        return render_page(request, 'login.html')
    
    elif request.method =='POST':
        start_time = time.perf_counter()
        username = request.POST.get("username")
        password = request.POST.get("password")  

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT password_hash FROM shop_user WHERE username = '{username}'")   
            credentials = cursor.fetchone() 

        if credentials is not None:
            if check_password(credentials[0], password):
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                auth_logger.log_auth(request.META.get('REMOTE_ADDR'), username, 'success', latency_ms)
                sign = signature(username, Cookie_key)
                response = redirect('/profile')
                response.set_cookie(key='session', value=sign, max_age=60*60*24*7)
                return response
            
            else:
                end_time = time.perf_counter()
                latency_ms = (end_time - start_time) * 1000
                context = {'error': 'wrong password'}
                auth_logger.log_auth(request.META.get('REMOTE_ADDR'), username, 'wrong_password', latency_ms)
                return render_page(request, 'login.html', context)
            
        else:
            end_time = time.perf_counter()
            latency_ms = (end_time - start_time) * 1000
            context = {'error': 'invalid username'}
            auth_logger.log_auth(request.META.get('REMOTE_ADDR'), username, 'invalid_user', latency_ms)
            return render_page(request, 'login.html', context)



def profile(request):
    cookies = request.COOKIES.get('session')
    if cookies is not None:
        username = cookies.split(':')[0]
        if verify_signature(Cookie_key, cookies):
            context = {'name': username}
            return render_page(request, 'profile.html', context)
        return redirect('/login/')
    return redirect('/login/')

def register(request):
    if request.method == 'GET':
        return render_page(request, 'register.html')
    elif request.method == 'POST':
        start_time = time.perf_counter()
        username = request.POST.get("username")
        password = request.POST.get("password")
        hashed_pas = hash_pas(password)
        try:
            User.create_user(username, hashed_pas)
        except ValueError:
            context = {'error': 'имя пользлвателя занято'}
            return render_page(request, 'register.html', context)
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        auth_logger.log_auth(request.META.get('REMOTE_ADDR'), username, 'registered', latency_ms)
        return redirect('/login/')
        

def logout(request):
    response = HttpResponse()
    start_time = time.perf_counter()
    if request.COOKIES.get('session'):
        username = request.COOKIES.get('session').split(':')[0]
        response = redirect('/')
        response.delete_cookie('session')
        end_time = time.perf_counter()
        latency_ms = (end_time - start_time) * 1000
        auth_logger.log_auth(request.META.get('REMOTE_ADDR'), username, 'logout', latency_ms)
        return response
    return redirect('/')

def search(request):
    payload = request.GET.get('q')
    context = {'result': [],
               'q': payload
               }
    if payload:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM shop_Product WHERE name ILIKE '%{payload}%';")
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context.update({'result': rows})

    return render_page(request, 'search.html', context)
