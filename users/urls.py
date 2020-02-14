from django.urls import path
from .views import login, logout, authorize

urlpatterns = [
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('authorize/', authorize, name="authorize"),
]