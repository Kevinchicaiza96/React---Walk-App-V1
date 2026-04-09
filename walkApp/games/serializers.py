# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import HistorialJuegoTrivia, EstadisticasUsuarioTrivia, HistorialMapaRoto


class HistoriaSerializer(serializers.ModelSerializer):
    porcentaje_acierto = serializers.ReadOnlyField()
    calificacion = serializers.ReadOnlyField()

    class Meta:
        model = HistorialJuegoTrivia
        fields = [
            'id', 'usuario', 'categoria', 'puntos',
            'respuestas_correctas', 'respuestas_incorrectas',
            'fecha_juego', 'duracion_segundos',
            'porcentaje_acierto', 'calificacion',
        ]
        read_only_fields = ['id', 'usuario', 'fecha_juego']

class EstadisticasSerializer(serializers.ModelSerializer):
    promedio_puntos = serializers.ReadOnlyField()
    tasa_acierto_global = serializers.ReadOnlyField()

    class Meta:
        model = EstadisticasUsuarioTrivia
        fields = [
            'usuario', 'total_juegos', 'total_puntos', 'mejor_puntaje',
            'categoria_favorita', 'total_correctas', 'total_incorrectas',
            'ultima_actualizacion', 'promedio_puntos', 'tasa_acierto_global',
        ]
        read_only_fields = ['usuario', 'ultima_actualizacion']

class MapaRotoSerializer(serializers.ModelSerializer):
    pistas_restantes = serializers.ReadOnlyField()

    class Meta:
        model = HistorialMapaRoto
        fields = [
            'id', 'usuario', 'dificultad', 'imagen_mapa',
            'duracion_segundos', 'pistas_usadas', 'fecha_juego',
            'pistas_restantes',
        ]
        read_only_fields = ['id', 'usuario', 'fecha_juego']