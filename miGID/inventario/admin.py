from django.contrib import admin

# Register your models here.

from .models import Sede, Articulo, Proveedores

admin.site.register(Sede)
admin.site.register(Articulo)
admin.site.register(Proveedores)