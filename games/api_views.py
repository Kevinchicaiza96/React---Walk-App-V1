from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils import timezone
from .models import HistorialJuegoTrivia, EstadisticasUsuarioTrivia


@api_view(['POST'])
@permission_classes([AllowAny])
def api_guardar_resultado(request):
    """
    POST /api/juegos/guardar-resultado/
    Guarda el resultado de una partida de trivia.
    """
    categoria = request.data.get('categoria')
    puntos = int(request.data.get('puntos', 0))
    respuestas_correctas = int(request.data.get('respuestas_correctas', 0))
    respuestas_incorrectas = int(request.data.get('respuestas_incorrectas', 0))
    duracion_segundos = request.data.get('duracion_segundos')

    categorias_validas = [c[0] for c in HistorialJuegoTrivia.CATEGORIAS_CHOICES]
    if not categoria or categoria not in categorias_validas:
        return Response({'success': False, 'error': 'Categoría inválida.'}, status=400)

    if request.user.is_authenticated:
        juego = HistorialJuegoTrivia.objects.create(
            usuario=request.user,
            categoria=categoria,
            puntos=puntos,
            respuestas_correctas=respuestas_correctas,
            respuestas_incorrectas=respuestas_incorrectas,
            duracion_segundos=duracion_segundos,
            fecha_juego=timezone.now(),
        )
        return Response({
            'success': True,
            'juego_id': juego.id,
            'calificacion': juego.calificacion,
            'porcentaje': juego.porcentaje_acierto,
        }, status=201)

    return Response({'success': True, 'guest': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_estadisticas_trivia(request):
    """
    GET /api/juegos/estadisticas/
    Devuelve estadísticas y últimos 10 juegos del usuario.
    """
    try:
        stats = EstadisticasUsuarioTrivia.objects.get(usuario=request.user)
        estadisticas = {
            'total_juegos': stats.total_juegos,
            'total_puntos': stats.total_puntos,
            'mejor_puntaje': stats.mejor_puntaje,
            'promedio_puntos': stats.promedio_puntos,
            'tasa_acierto': stats.tasa_acierto_global,
            'categoria_favorita': stats.get_categoria_favorita_display() if stats.categoria_favorita else None,
        }
    except EstadisticasUsuarioTrivia.DoesNotExist:
        estadisticas = {
            'total_juegos': 0, 'total_puntos': 0, 'mejor_puntaje': 0,
            'promedio_puntos': 0, 'tasa_acierto': 0, 'categoria_favorita': None,
        }

    ultimos = HistorialJuegoTrivia.objects.filter(usuario=request.user).order_by('-fecha_juego')[:10]
    juegos_data = [{
        'id': j.id,
        'categoria': j.get_categoria_display(),
        'categoria_key': j.categoria,
        'puntos': j.puntos,
        'respuestas_correctas': j.respuestas_correctas,
        'respuestas_incorrectas': j.respuestas_incorrectas,
        'calificacion': j.calificacion,
        'porcentaje': j.porcentaje_acierto,
        'fecha': j.fecha_juego.strftime('%d/%m/%Y %H:%M'),
        'duracion_segundos': j.duracion_segundos,
    } for j in ultimos]

    return Response({'estadisticas': estadisticas, 'ultimos_juegos': juegos_data})