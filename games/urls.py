from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.mostrarJuegos, name='juegos'),
    path('mapa_roto/', views.mostrarMapaRoto, name='mapa_roto'),
    path('trivia/', views.trivia_inicio, name='trivia_inicio'),
    path('trivia/menu/', views.trivia_menu, name='juegos/trivia/menu/'),
    path('trivia/juego/', views.trivia_juego, name='trivia/juego/'),
    path('trivia/final/', views.trivia_final, name='trivia/final/'),
    path('api/guardar-resultado/', views.guardar_resultado, name='guardar_resultado'),
    path('api/estadisticas/', views.obtener_estadisticas, name='obtener_estadisticas'),
    path('trivia/historial/', views.historial_completo, name='historial_trivia'),

    # ============================
    # API REST (para React)
    # ============================
    path('api/juegos/guardar-resultado/', api_views.api_guardar_resultado, name='api_guardar_resultado'),
    path('api/juegos/estadisticas/', api_views.api_estadisticas_trivia, name='api_estadisticas_trivia'),
]