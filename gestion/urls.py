from django.urls import path
from . import views
from .views import (
    lista_pedidos, visualizar_pedido, cambiar_estado_pedido, 
    ProductoListView, ProductoCreateView, ProductoUpdateView, ProductoDeleteView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('productos/', views.lista_productos, name='lista_productos'),
    
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),

    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),

    path('tomar_pedido/', views.tomar_pedido, name='tomar_pedido'),

    path('guardar_pedido/', views.guardar_pedido, name='guardar_pedido'), 

    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),

    path('pedido/<int:pedido_id>/', visualizar_pedido, name='visualizar_pedido'),

    path('pedido/cambiar_estado/<int:pedido_id>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),

    path('productos/', ProductoListView.as_view(), name='productos'),

    path('producto/nuevo/', ProductoCreateView.as_view(), name='crear_producto'),

    path('producto/editar/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),

    path('producto/borrar/<int:pk>/', ProductoDeleteView.as_view(), name='borrar_producto'),


]