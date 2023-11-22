"""miGID URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView

from inventario.views import filtro, login_view, index, add_proveedor, add_sede, add_articulo, registro

from django.conf.urls import handler403

handler403 = 'inventario.views.error_view'

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
    path('inventario/', filtro, name='inventario'),

    path('añadir-proveedor/', add_proveedor, name='add_proveedor'),
    path('añadir-sede/', add_sede, name='add_sede'),
    path('añadir-articulo/', add_articulo, name='add_articulo'),

    path('registro/', registro, name='registro'),

    path('login/', login_view, name='login'),

    path('logout/', LogoutView.as_view(), name='logout'),
]


