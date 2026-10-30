from django.db import models

# Create your models here.
class perfil (models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    estatus = models.BooleanField(default=True)