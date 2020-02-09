from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, "app1_login.html", {"client_id": 1})

def auth_landing_page(request):
    code = request.GET['code']
    state = request.GET['state']
    return render(request, "app1_auth_landing_page.html", { 
        "code": code, 
        "state": state 
    })