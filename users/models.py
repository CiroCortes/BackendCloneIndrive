from django.db import models

# Create your models here.
# create a model for the user
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    image = models.CharField(max_length=255, null=True, blank=True) ##blank para que no sea requerido
    password = models.CharField(max_length=255)
    notification_token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'

    
