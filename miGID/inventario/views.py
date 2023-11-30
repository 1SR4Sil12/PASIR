from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from inventario.models import Articulo, Sede, Proveedores, Pedido
from django.forms import ModelForm
from django.http import HttpResponse

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required

# Formulario para cada modelo

class ProveedorForm(ModelForm):
    class Meta:
        model = Proveedores
        fields = ['cod', 'nom']

class SedeForm(ModelForm):
    class Meta:
        model = Sede
        fields = ['nom', 'cod']

class ArticuloForm(ModelForm):
    class Meta:
        model = Articulo
        fields = ['sede', 'proveedor', 'nom', 'cod', 'fecha_stock', 'des', 'pvp']

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['articulo', 'cantidad']

# Vistas para creación

@permission_required('inventario.add_proveedores', raise_exception=True)
@login_required
def add_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ProveedorForm()
    if not request.user.has_perm('inventario.add_proveedores'):
        raise PermissionDenied
    return render(request, 'inventario/add_proveedor.html', {'form': form})

@permission_required('inventario.add_sede', raise_exception=True)
@login_required
def add_sede(request):
    if request.method == 'POST':
        form = SedeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = SedeForm()
    if not request.user.has_perm('inventario.add_sede'):
        raise PermissionDenied
    return render(request, 'inventario/add_sede.html', {'form': form})

@permission_required('inventario.add_articulo', raise_exception=True)
@login_required
def add_articulo(request):
    if request.method == 'POST':
        form = ArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ArticuloForm()
    if not request.user.has_perm('inventario.add_articulo'):
        raise PermissionDenied
    return render(request, 'inventario/add_articulo.html', {'form': form})

# Vista para Pedidos

@login_required
def crear_pedido(request, articulo_id):
    articulo = get_object_or_404(Articulo, id=articulo_id)
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.usuario = request.user
            pedido.articulo = articulo
            pedido.save()
            return redirect('index')
    else:
        form = PedidoForm()

    return render(request, 'inventario/pedido.html', {'form': form, 'articulo': articulo})

def mis_pedidos(request):
    if request.user.is_authenticated:
        pedidos = Pedido.objects.filter(usuario=request.user)
        return render(request, 'inventario/mis_pedidos.html', {'pedidos': pedidos})

def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    if request.method == 'POST':
        pedido.delete()
        return redirect('mis_pedidos')
    return render(request, 'confirmar_eliminacion.html', {'pedido': pedido})

# Vista eliminar articulos

@login_required
@permission_required('inventario.delete_articulo', raise_exception=True)
def delete_articulo(request, id):
    articulo = get_object_or_404(Articulo, id=id)
    if request.method == "POST":
        articulo.delete()
        return redirect('inventario')
    else:
        return redirect('inventario')

# Vista error

def error_view(request, exception):
    return render(request, 'inventario/403.html', {}, status=403)

# Vista para registro de Usuarios

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'inventario/registro.html', {'form': form})

# Vista para login

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la vista de index
        else:
            # Mensaje de error de login
            return render(request, 'login.html', {'error': 'Usuario o contraseña inválidos'})
    return render(request, 'inventario/login.html')

# Vista para el index

def index(request):
    return render(request, 'inventario/index.html')

# Vista para el filtro del inventario

@login_required
def filtro(request):
    sedes = Sede.objects.all()
    proveedores = Proveedores.objects.all()
    articulos = None

    if request.method == 'POST':
        sede_id = request.POST.get('sede')
        nombre_articulo = request.POST.get('nombre_articulo')
        proveedor_id = request.POST.get('proveedor')
        precio_minimo = request.POST.get('precio_minimo')
        precio_maximo = request.POST.get('precio_maximo')
        fecha_stock = request.POST.get('fecha_stock')
        codigo_articulo = request.POST.get('codigo_articulo')

        articulos = Articulo.objects.all()

        if sede_id:
            articulos = articulos.filter(sede_id=sede_id)
        if nombre_articulo:
            articulos = articulos.filter(nom__icontains=nombre_articulo)
        if proveedor_id:
            articulos = articulos.filter(proveedor_id=proveedor_id)
        if precio_minimo:
            articulos = articulos.filter(pvp__gte=precio_minimo)
        if precio_maximo:
            articulos = articulos.filter(pvp__lte=precio_maximo)
        if fecha_stock:
            articulos = articulos.filter(fecha_stock__date=fecha_stock)
        if codigo_articulo:
            articulos = articulos.filter(cod__icontains=codigo_articulo)

    return render(request, 'inventario/filtro.html', {'sedes': sedes, 'proveedores': proveedores, 'articulos': articulos})
