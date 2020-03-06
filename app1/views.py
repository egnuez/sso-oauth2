from django.shortcuts import render
from urllib import request as urlrequest
from urllib import parse
import json
import jwt
import base64

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
        token = data["token"]
        token_info = data["token"].split(".")[1]
        token_info = json.loads(base64.b64decode( token_info + "=" * ((4 - len(token_info) % 4) % 4) ))
        return render(request, "app1_auth_landing_page.html", { 
            "resource_id":token_info["resource_id"],
            "user_id":token_info["user_id"],
            "client_id":token_info["client_id"],
            "token": data["token"],
        })