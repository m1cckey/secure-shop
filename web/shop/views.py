from django.shortcuts import render
from django.db import connection



def render_page(request, template, context=None):
    return render(request, template, context or {})

def index(request):
    return render_page(request, 'index.html')

def login(request):
    return render_page(request, 'login.html')

def register(request):
    return render_page(request, 'register.html')

def search(request):
    payload = request.GET.get('q')
    context = {'result': [],
               'q': payload
               }
    if payload:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM shop_Product WHERE name LIKE '%{payload}%';")
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            context.update({'result': rows})

    return render_page(request, 'search.html', context)

def profile(request):
    return render_page(request, 'profile.html')