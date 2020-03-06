from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import datetime
import jwt

from .models import Apps, Users, Resources

# Create your views here.

def login(request):
    
    username = request.GET['username']
    password = request.GET['password']

    response_type = request.GET['response_type']
    client_id = request.GET['client_id']
    resource_id = request.GET['resource_id']
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

        return redirect("/users/authorize?response_type={}&client_id={}&resource_id={}&redirect_uri={}&state={}&scope={}".format(
            response_type,
            client_id,
            resource_id,
            redirect_uri,
            state,
            scope
        ))
    except Users.DoesNotExist:
        return render(request, "login_fail.html")

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def authorize(request):

    response_type = request.GET['response_type']
    client_id = request.GET['client_id']
    redirect_uri = request.GET['redirect_uri']
    state = request.GET['state']
    scope = request.GET['scope']
    resource_id = request.GET['resource_id']
    granted = request.GET.get('granted', 'no') == "yes"

    if 'user' not in request.session:

        return render(request, "login.html", {
            "response_type": response_type,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "resource_id": resource_id,
            "state": state,
            "scope": scope,
        }) 

    
    if granted:

        #
        # Validate client_id, and user_id permissions before response
        #

        code = jwt.encode({
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30),
            'client_id': client_id,
            'user_id': 1,
            "resource_id": resource_id,
        }, 'secret_code', algorithm='HS256')
        url = "{}/?code={}&state={}".format(redirect_uri, code.decode('ascii'), state) 
        return redirect(url)
        
    try:

        app = Apps.objects.get(id = client_id)
        resource = Resources.objects.get(id = resource_id)

        if not Users.objects.filter(id=app.id).exists():
            return render(request, "error.html", {
                "error": "El usuario no tiene permisos para esta operacion"
            })

        if not Resources.objects.filter(id=app.id).exists():
            return render(request, "error.html", {
                "error": "La app no tiene permisos para esta operacion"
            })

        return render(request, "permisions.html", {
            "app":{
                "id": app.id,
                "name": app.name,
            },
            "resource":{
                "id": resource.id,
                "name": resource.name,
            },
            "user": request.session['user'],
            "response_type": response_type,
            "client_id": client_id,
            "resource_id": resource_id,
            "redirect_uri": redirect_uri,
            "state": state,
            "scope": scope,
            "resource_id":resource_id,
        })

    except Apps.DoesNotExist:
        return render(request, "error.html", {
            "error": "La App solicitada no existe"
        })
    except Resources.DoesNotExist:
        return render(request, "error.html", {
            "error": "El Recurso solicitado no existe"
        })
    
def token(request):
    try:
        code_content = jwt.decode(request.GET['code'], 'secret_code', algorithms=['HS256'])
        app = Apps.objects.get(id = request.GET['client_id'], secret = request.GET['app_secret'])
        token = jwt.encode({
            'client_id': request.GET['client_id'],
            'user_id': code_content['user_id'],
            'resource_id': code_content['resource_id'],
        }, 'secret_token', algorithm='HS256')
    except jwt.exceptions.InvalidSignatureError:
        return HttpResponse('Invalid Signature', status=403)
    except jwt.exceptions.ExpiredSignatureError:
        return HttpResponse('Expired Signature', status=403)
    except Apps.DoesNotExist:
        return HttpResponse('App does not exists', status=403)

    return JsonResponse({
        "token": token.decode('utf-8')
    })
