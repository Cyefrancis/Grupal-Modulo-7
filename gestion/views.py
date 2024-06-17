from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Producto, Pedido, DetallePedido
from django.urls import reverse, reverse_lazy
from .forms import ProductoForm
import decimal as Decimal
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
    pedidos = Pedido.objects.all()  # Obtiene todos los pedidos de la base de datos
    context = {'pedidos': pedidos}
    return render(request, 'gestion/lista_pedidos.html', context)

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
        cantidades = request.POST.get('cantidades')
        precios_unitarios = request.POST.get('precios_unitarios')

        # Validación inicial de datos requeridos
        if not cliente or not direccion or not productos or not cantidades or not precios_unitarios:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('tomar_pedido')

        try:
            # Convertir las cantidades y precios a listas
            cantidades_list = [int(c.strip()) for c in cantidades.split(',')]
            precios_list = [Decimal(p.strip()) for p in precios_unitarios.split(',')]
        except Exception as e:
            messages.error(request, f"Error al procesar cantidades o precios: {str(e)}")
            return redirect('tomar_pedido')

        # Validar que las listas de productos, cantidades y precios tienen la misma longitud
        if len(productos) != len(cantidades_list) or len(cantidades_list) != len(precios_list):
            messages.error(request, "Las listas de productos, cantidades y precios deben tener la misma longitud.")
            return redirect('tomar_pedido')

        try:
            pedido = Pedido(cliente=cliente, direccion_entrega=direccion)
            pedido.save()

            for producto_id, cantidad, precio_unitario in zip(productos, cantidades_list, precios_list):
                producto = Producto.objects.get(id=producto_id)
                detalle = DetallePedido(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario
                )
                detalle.save()

            messages.success(request, "Pedido guardado exitosamente.")
            return redirect('lista_pedidos')
        except Exception as e:
            messages.error(request, f"Error al guardar el pedido: {str(e)}")
            return redirect('tomar_pedido')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('tomar_pedido')
    
def visualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'gestion/visualizar_pedido.html', {
        'pedido': pedido,
        'detalles': detalles
    })

def cambiar_estado_pedido(request, pedido_id):
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        return HttpResponseRedirect(reverse('visualizar_pedido', args=[pedido_id]))
    
class ProductoListView(ListView):
    model = Producto
    template_name = 'gestion/productos.html'
    context_object_name = 'productos'

class ProductoCreateView(CreateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock']
    template_name = 'gestion/form_producto.html'
    success_url = reverse_lazy('productos')

class ProductoUpdateView(UpdateView):
    model = Producto
    fields = ['nombre', 'descripcion', 'precio', 'stock']
    template_name = 'gestion/form_producto.html'
    success_url = reverse_lazy('productos')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'gestion/confirmar_borrar.html'
    success_url = reverse_lazy('productos')