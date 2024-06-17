from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido
from .forms import ProductoForm
import decimal
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

def tomar_pedido(request):
    productos = Producto.objects.all()
    return render(request, 'gestion/tomar_pedido.html', {'productos': productos})

def guardar_pedido(request):
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        direccion = request.POST.get('direccion')
        productos = request.POST.getlist('productos')
        cantidades = request.POST.getlist('cantidades')
        precios_unitarios = request.POST.getlist('precios_unitarios')

        if not cliente or not direccion or not productos or not cantidades or not precios_unitarios:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('tomar_pedido')

        pedido = Pedido(cliente=cliente, direccion_entrega=direccion)
        pedido.save()

        for producto_id, cantidad, precio_unitario in zip(productos, cantidades, precios_unitarios):
            producto = Producto.objects.get(id=producto_id)
            detalle = DetallePedido(
                pedido=pedido,
                producto=producto,
                cantidad=int(cantidad),
                precio_unitario=decimal.Decimal(precio_unitario)
            )
            detalle.save()

        messages.success(request, "Pedido guardado exitosamente.")
        return redirect('lista_pedidos')

    else:
        messages.error(request, "Método no permitido.")
        return redirect('tomar_pedido')