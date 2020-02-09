from django.urls import path
from .views import login, logout, authorize, auth

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('authorize/', authorize, name="authorize"),
    path('auth/', auth),
]