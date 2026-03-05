from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    # Vista Django original (templates)
    path('comunidad', views.mostrarComunidad, name='comunidad'),

    # ============================
    # API REST (para React)
    # ============================
    path('api/comunidad/', api_views.api_lista_publicaciones, name='api_lista_publicaciones'),
    path('api/comunidad/crear/', api_views.api_crear_publicacion, name='api_crear_publicacion'),
    path('api/comunidad/<int:pub_id>/eliminar/', api_views.api_eliminar_publicacion, name='api_eliminar_publicacion'),
    path('api/comunidad/<int:pub_id>/comentarios/', api_views.api_comentarios_publicacion, name='api_comentarios_publicacion'),
    path('api/comunidad/<int:pub_id>/comentarios/crear/', api_views.api_crear_comentario_pub, name='api_crear_comentario_pub'),
]