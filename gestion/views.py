from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
# Create your views here.

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'gestion/lista_productos.html', {'productos': productos})

@login_required
@permission_required('usuarios.can_add_product', raise_exception=True)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'gestion/agregar_producto.html', {'form': form})

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'gestion/lista_pedidos.html', {'pedidos': pedidos})

def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'gestion/detalle_pedido.html', {'pedido': pedido, 'detalles': detalles})