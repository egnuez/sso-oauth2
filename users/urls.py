from django.urls import path
from .views import login, logout, authorize, auth

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('authorize/', authorize, name="authorize"),
    path('auth/', auth, name="auth"),
]