# con esto creamos un serializador para el modelo User
from rest_framework import serializers
from .models import User
import bcrypt; #para encriptar la contraseña

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'lastname', 'email', 'phone', 'image','password','notification_token']
        extra_kwargs = { #extra_kwargs es para que el password no se muestre en la respuesta
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        raw_password = validated_data.pop('password')
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt())
        validated_data['password'] = hashed_password.decode('utf-8')
        user = User.objects.create(**validated_data)
        return user

        