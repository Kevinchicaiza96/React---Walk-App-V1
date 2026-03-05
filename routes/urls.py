from django.urls import path
from . import views
from .models import ComentarioRuta
from . import api_views

urlpatterns = [
    path('rutas/', views.mostrarRutas, name='rutas'),

    # ============================
    # CRUD DE RUTAS (USUARIO)
    # ============================
    path('rutas/crear/', views.crear_ruta, name='crear_ruta'),
    path('rutas/<int:ruta_id>/', views.detalle_ruta, name='detalle_ruta'),
    path('rutas/eliminar/<int:pk>/', views.eliminar_ruta, name='eliminar_ruta'),
    path('rutas/<int:ruta_id>/qr/', views.generar_qr_ruta, name='generar_qr_ruta'),

    # FAVORITAS
    path('rutas/<int:ruta_id>/marcar-favorita/', views.marcar_favorita, name='marcar_favorita'),
    path('rutas/<int:ruta_id>/quitar-favorita/', views.quitar_favorita, name='quitar_favorita'),

    # TRACKING
    path('rutas/<int:ruta_id>/iniciar/', views.iniciar_ruta, name='iniciar_ruta'),
    path('rutas/<int:ruta_id>/terminar/', views.terminar_ruta, name='terminar_ruta'),
    path('api/guardar-posicion/', views.guardar_posicion, name='guardar_posicion'),

    # ============================
    # API REST (para React)
    # ============================
    path('api/rutas/', api_views.api_lista_rutas, name='api_lista_rutas'),
    path('api/rutas/<int:ruta_id>/', api_views.api_detalle_ruta, name='api_detalle_ruta'),

    path('api/rutas/<int:ruta_id>/comentarios/', api_views.api_comentarios_ruta, name='api_comentarios_ruta'),
    path('api/rutas/<int:ruta_id>/comentarios/crear/', api_views.api_crear_comentario, name='api_crear_comentario'),
    path('api/rutas/<int:ruta_id>/comentarios/eliminar/', api_views.api_eliminar_comentario, name='api_eliminar_comentario'),
]