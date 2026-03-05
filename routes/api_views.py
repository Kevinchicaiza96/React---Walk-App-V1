from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Ruta
from .serializers import RutaSerializer


@api_view(['GET'])
def api_lista_rutas(request):
    """
    Endpoint público que devuelve todas las rutas en JSON.
    Soporta filtros por dificultad y búsqueda por nombre.

    GET /api/rutas/
    GET /api/rutas/?dificultad=FACIL
    GET /api/rutas/?buscar=cerro
    GET /api/rutas/?dificultad=MODERADO&buscar=tabor
    """
    rutas = Ruta.objects.all().order_by('nombre_ruta')

    dificultad = request.GET.get('dificultad')
    buscar = request.GET.get('buscar')

    if dificultad:
        rutas = rutas.filter(dificultad__iexact=dificultad)
    if buscar:
        rutas = rutas.filter(nombre_ruta__icontains=buscar)

    serializer = RutaSerializer(rutas, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def api_detalle_ruta(request, ruta_id):
    """
    Endpoint que devuelve el detalle de una ruta específica.

    GET /api/rutas/<id>/
    """
    try:
        ruta = Ruta.objects.get(id=ruta_id)
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada'}, status=404)

    serializer = RutaSerializer(ruta, context={'request': request})
    return Response(serializer.data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Avg, Count
from .models import Ruta, ComentarioRuta
from .serializers import RutaSerializer


@api_view(['GET'])
def api_lista_rutas(request):
    rutas = Ruta.objects.all().order_by('nombre_ruta')
    dificultad = request.GET.get('dificultad')
    buscar = request.GET.get('buscar')
    if dificultad:
        rutas = rutas.filter(dificultad__iexact=dificultad)
    if buscar:
        rutas = rutas.filter(nombre_ruta__icontains=buscar)
    serializer = RutaSerializer(rutas, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def api_detalle_ruta(request, ruta_id):
    try:
        ruta = Ruta.objects.get(id=ruta_id)
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada'}, status=404)
    serializer = RutaSerializer(ruta, context={'request': request})
    return Response(serializer.data)


# ─── COMENTARIOS ──────────────────────────────────────────────────────────────

@api_view(['GET'])
@permission_classes([AllowAny])
def api_comentarios_ruta(request, ruta_id):
    """
    GET /api/rutas/<id>/comentarios/
    Devuelve todos los comentarios de una ruta + stats de rating.
    """
    try:
        ruta = Ruta.objects.get(id=ruta_id)
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada'}, status=404)

    comentarios = ComentarioRuta.objects.filter(ruta=ruta).select_related('usuario')

    # Stats de rating
    stats = comentarios.aggregate(
        promedio=Avg('estrellas'),
        total=Count('id')
    )

    # Distribución por estrellas
    distribucion = {}
    for i in range(1, 6):
        distribucion[str(i)] = comentarios.filter(estrellas=i).count()

    # Serializar comentarios
    data = []
    for c in comentarios:
        data.append({
            'id': c.id,
            'usuario': c.usuario.username,
            'nombre_completo': f"{c.usuario.first_name} {c.usuario.last_name}".strip() or c.usuario.username,
            'texto': c.texto,
            'estrellas': c.estrellas,
            'fecha': c.fecha.strftime('%d de %B de %Y'),
        })

    return Response({
        'comentarios': data,
        'stats': {
            'promedio': round(stats['promedio'] or 0, 1),
            'total': stats['total'],
            'distribucion': distribucion,
        }
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_crear_comentario(request, ruta_id):
    """
    POST /api/rutas/<id>/comentarios/crear/
    Crea o actualiza el comentario del usuario en la ruta.
    """
    try:
        ruta = Ruta.objects.get(id=ruta_id)
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada'}, status=404)

    texto = request.data.get('texto', '').strip()
    estrellas = request.data.get('estrellas', 5)

    if not texto:
        return Response({'error': 'El comentario no puede estar vacío.'}, status=400)

    try:
        estrellas = int(estrellas)
        if not (1 <= estrellas <= 5):
            raise ValueError
    except (ValueError, TypeError):
        return Response({'error': 'Las estrellas deben ser entre 1 y 5.'}, status=400)

    # Crear o actualizar (un comentario por usuario por ruta)
    comentario, creado = ComentarioRuta.objects.update_or_create(
        ruta=ruta,
        usuario=request.user,
        defaults={'texto': texto, 'estrellas': estrellas}
    )

    return Response({
        'id': comentario.id,
        'usuario': comentario.usuario.username,
        'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'texto': comentario.texto,
        'estrellas': comentario.estrellas,
        'fecha': comentario.fecha.strftime('%d de %B de %Y'),
        'creado': creado,
    }, status=201 if creado else 200)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_eliminar_comentario(request, ruta_id):
    """
    DELETE /api/rutas/<id>/comentarios/eliminar/
    Elimina el comentario del usuario en la ruta.
    """
    try:
        comentario = ComentarioRuta.objects.get(ruta_id=ruta_id, usuario=request.user)
        comentario.delete()
        return Response({'mensaje': 'Comentario eliminado.'})
    except ComentarioRuta.DoesNotExist:
        return Response({'error': 'No tienes comentario en esta ruta.'}, status=404)