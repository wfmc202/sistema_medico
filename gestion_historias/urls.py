from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_historia_clinica, name='crear_historia_clinica'),
    path('detalle/<int:historia_id>/', views.detalle_historia_clinica, name='detalle_historia_clinica'),
    path('listar/', views.listar_historias_clinicas, name='listar_historias_clinicas'),
    # Podríamos añadir una URL raíz para la app si es necesario, por ejemplo:
    # path('', views.listar_historias_clinicas, name='lista_historias_raiz'),
]
