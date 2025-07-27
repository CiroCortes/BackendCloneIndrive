from django.urls import path
from users.views import update
from users.views import updateWhitImage

urlpatterns = [
    path('/<id_user>', update),
    path('/upload/<id_user>', updateWhitImage),

   #path('/login', login),
]
