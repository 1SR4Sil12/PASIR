from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.

class Sede(models.Model):
	nom = models.CharField('Nombre', max_length=50)
	cod = models.CharField('Código', max_length=3)

	def __str__(self):
		return f'{self.nom}'

class Proveedores(models.Model):
	cod = models.IntegerField('Código', default=0)
	nom = models.CharField('Nombre', max_length=50)

	def __str__(self):
		return f'{self.nom}'


class Articulo(models.Model):
	sede = models.ForeignKey(Sede, on_delete=models.CASCADE)
	proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True)
	nom = models.CharField('Nombre', max_length=50)
	cod = models.CharField('Código', max_length=9)
	fecha_stock = models.DateTimeField('Fecha de Stock', default=datetime.datetime.now)
	des = models.TextField('Descripción')
	pvp = models.IntegerField('Precio')

	def __str__(self):
		return f'{self.nom} {self.pvp} €'

	class Meta:
		verbose_name_plural = "Artículos"


class Perfil(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
	ape = models.CharField('Apellidos', max_length=50)

	def __str__(self):
		return f'{self.user} {self.ape}'

	class Meta:
		verbose_name_plural = "Perfiles"
