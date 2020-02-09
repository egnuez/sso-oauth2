from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import datetime
import jwt

from .models import Apps, Users

# Create your views here.

def login(request):
    
    username = request.GET['username']
    password = request.GET['password']

    response_type = request.GET['response_type']
    client_id = request.GET['client_id']
    redirect_uri = request.GET['redirect_uri']
    state = request.GET['state']
    scope = request.GET['scope']
    
    try:
        user = Users.objects.get(username = username, password = password)
        request.session['user'] = {
            "logged": True,
            "username": user.username,
            "id": user.id,
        }

        return redirect("/users/auth?response_type={}&client_id={}&redirect_uri={}&state={}&scope={}".format(
            response_type,
            client_id,
            redirect_uri,
            state,
            scope,
        ))
    except Users.DoesNotExist:
        return render(request, "login_fail.html")

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def auth(request):

    response_type = request.GET['response_type']
    client_id = request.GET['client_id']
    redirect_uri = request.GET['redirect_uri']
    state = request.GET['state']
    scope = request.GET['scope']

    if 'user' in request.session:
        try:
            app = Apps.objects.get(id = client_id)
            return render(request, "permisions.html", {
                "app":{
                    "id": app.id,
                    "name": app.name,
                },
                "user": request.session['user'],
                "response_type": response_type,
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "state": state,
                "scope": scope,
            })
        except Apps.DoesNotExist:
            return render(request, "app_does_not_exist.html", {
                "client_id": client_id
            })
    else:
        return render(request, "login.html", {
            "response_type": response_type,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": scope,
        })

def authorize(request):
    
    response_type = request.GET['response_type']
    client_id = request.GET['client_id']
    redirect_uri = request.GET['redirect_uri']
    state = request.GET['state']
    scope = request.GET['scope']

    code = jwt.encode({
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
        'client_id': client_id,
        'user_id': 1,
    }, 'secret_code', algorithm='HS256')
    url = "{}/?code={}&state={}".format(redirect_uri, code.decode('ascii'), state) 
    return redirect(url)

def token(request, client_id, app_secret, code):
    token = jwt.encode({
        'client_id': client_id,
        'user_id': 1,
    }, 'secret_token', algorithm='HS256')
 
    return JsonResponse({
        "token": token
    })
