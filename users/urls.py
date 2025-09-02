from django.urls import path
from users.views import update, get_user_by_id, updateWhitImage, get_all_users

urlpatterns = [
    path('<id_user>', update),
    path('findById/<id_user>', get_user_by_id),
    path('', get_all_users),
    path('upload/<id_user>', updateWhitImage),

   #path('/login', login),
]
