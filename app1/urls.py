from django.urls import path
from .views import login, auth_landing_page

urlpatterns = [
    path('login/', login),
    path('auth_landing_page/', auth_landing_page),
]