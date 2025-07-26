from django.db import models


# tabla pivote para la relacion many to many
class UserHasRole(models.Model):
    id_user = models.ForeignKey('users.User', on_delete=models.CASCADE,db_column='id_user')
    id_rol = models.ForeignKey('roles.Role', on_delete=models.CASCADE,db_column='id_rol')
    
    class Meta:
        db_table = 'users_has_roles'
        # este parametro la llave primaria es la combinacion de las dos columnas
        unique_together = ('id_user', 'id_rol')



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
    ## relacion con la tabla roles
    roles = models.ManyToManyField(
        'roles.Role', 
        through='UserHasRole', # aqui le decimos que la tabla pivote es UserHasRole
        related_name='users'
    )
    
    class Meta:
        db_table = 'users'

    
