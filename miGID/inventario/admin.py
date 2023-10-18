from django.contrib import admin

# Register your models here.

from .models import Sede, Articulo

admin.site.register(Sede)
admin.site.register(Articulo)