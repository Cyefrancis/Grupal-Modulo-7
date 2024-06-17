from django.contrib import admin
from .models import Producto, Pedido, DetallePedido
# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock']
    search_fields = ['nombre']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'estado', 'fecha_pedido', 'fecha_actualizacion']
    search_fields = ['cliente']
    list_filter = ['estado', 'fecha_pedido', 'fecha_actualizacion']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'producto', 'cantidad', 'precio_unitario']