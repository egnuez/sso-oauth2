from django.shortcuts import render
from urllib import request as urlrequest
from urllib import parse
import json

# Create your views here.

def login(request):
    return render(request, "app1_login.html", {"client_id": 1})

def auth_landing_page(request):
    code = request.GET['code']
    state = request.GET['state']

    params = {
        'client_id': 1,
        'app_secret': '1029384756',
        'code': code,
    }

    url_values = parse.urlencode(params)
    url = 'http://127.0.0.1:8000/users/token'
    full_url = url + '?' + url_values

    with urlrequest.urlopen(full_url) as response:
        data = json.loads(response.read())
        return render(request, "app1_auth_landing_page.html", { 
            "code": code, 
            "state": state,
            "token": data["token"],
        })