from rest_framework import serializers
from .models import Ruta


class RutaSerializer(serializers.ModelSerializer):
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = Ruta
        fields = [
            'id',
            'nombre_ruta',
            'descripcion',
            'longitud',
            'dificultad',
            'duracion_estimada',
            'ubicacion',
            'ubicacion_inicio',
            'ubicacion_fin',
            'puntos_interes',
            'vistas',
            'imagen_url',
        ]

    def get_imagen_url(self, obj):
        request = self.context.get('request')
        if obj.imagen and request:
            return request.build_absolute_uri(obj.imagen.url)
        return None