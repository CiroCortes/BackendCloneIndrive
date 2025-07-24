from django.urls import path
from .views import create, login

urlpatterns = [
    path('', create),
    path('/login', login),
]