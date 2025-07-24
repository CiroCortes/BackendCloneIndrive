from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User
import bcrypt

from .serializers import UserSerializer
# Create your views here.

@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'El email o el password son incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

    if  bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user_data = {
                'id': user.id,
                'name': user.name,
                'lastname': user.lastname,
                'email': user.email,
                'phone': user.phone,
                'image': user.image,
                'notification_token': user.notification_token
            }
            return Response(user_data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'El email o el password son incorrectos'}, 
                         status=status.HTTP_401_UNAUTHORIZED)