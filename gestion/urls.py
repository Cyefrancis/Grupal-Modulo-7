from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('tomar_pedido/', views.tomar_pedido, name='tomar_pedido'),
    path('guardar_pedido/', views.guardar_pedido, name='guardar_pedido'), 
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
]