from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from roles.models import Role
from roles.serializers import RoleSerializer
from users.models import User, UserHasRole
import bcrypt
from users.serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user =serializer.save()

        client_role = get_object_or_404(Role, id='CLIENT') # este metdo nos devuelve un rol y si no exite devuelve un error
        UserHasRole.objects.create(id_user=user, id_rol=client_role)
        roles = Role.objects.filter(userhasrole__id_user=user)
        roles_serializer = RoleSerializer(roles, many=True)
        response_data = {
            **serializer.data,
            'roles' : roles_serializer.data
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    error_messages = []
    for field, errors in serializer.errors.items():
        for error in errors:
            error_messages.append(f"{field}: {error}")

    error_response = {
        "message" : error_messages,
        "statusCode" : status.HTTP_400_BAD_REQUEST
    }
    return Response(error_response, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {
             "message": "Email and password are required",
             "statusCode" : status.HTTP_400_BAD_REQUEST
            },
             status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
           return Response(
              {
              "message": "Email or password are not valid",
              "statusCode" : status.HTTP_401_UNAUTHORIZED
              },
              status=status.HTTP_401_UNAUTHORIZED
           )

    if  bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)
            roles = Role.objects.filter(userhasrole__id_user=user)
            roles_serializer = RoleSerializer(roles, many=True)
            user_data = {
                 "user" : {
                    'id': user.id,
                    'name': user.name,
                    'lastname': user.lastname,
                    'email': user.email,
                    'phone': user.phone,
                    'image': user.image,
                    'notification_token': user.notification_token,
                    'roles': roles_serializer.data,

                 },
                'token': 'Bearer ' + access_token
               
            }
            return Response(user_data, status=status.HTTP_200_OK)
    else:
          return Response(
            {
             "message": "Email and password are required",
             "statusCode" : status.HTTP_401_UNAUTHORIZED
            },
             status=status.HTTP_401_UNAUTHORIZED
             )

# Create your views here.
