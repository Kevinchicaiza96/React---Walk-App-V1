from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.core.paginator import Paginator
from .models import Publicacion, Comentario


# ─── LISTAR PUBLICACIONES ─────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def api_lista_publicaciones(request):
    """
    GET /api/comunidad/
    Devuelve publicaciones paginadas, ordenadas por fecha desc.
    """
    publicaciones = Publicacion.objects.all().order_by('-fecha_publicacion').select_related('usuario', 'ruta')

    # Filtro por ruta opcional
    ruta_id = request.GET.get('ruta')
    if ruta_id:
        publicaciones = publicaciones.filter(ruta_id=ruta_id)

    # Paginación
    pagina = request.GET.get('pagina', 1)
    paginador = Paginator(publicaciones, 10)
    pagina_obj = paginador.get_page(pagina)

    data = []
    for p in pagina_obj:
        total_comentarios = p.comentarios.count()
        data.append({
            'id': p.id,
            'usuario': p.usuario.username,
            'nombre_completo': f"{p.usuario.first_name} {p.usuario.last_name}".strip() or p.usuario.username,
            'ruta_id': p.ruta.id,
            'ruta_nombre': p.ruta.nombre_ruta,
            'comentario': p.comentario,
            'imagen': request.build_absolute_uri(p.imagen.url) if p.imagen else None,
            'fecha': p.fecha_publicacion.strftime('%d de %B de %Y · %H:%M'),
            'total_comentarios': total_comentarios,
        })

    return Response({
        'publicaciones': data,
        'total': paginador.count,
        'paginas': paginador.num_pages,
        'pagina_actual': pagina_obj.number,
        'tiene_siguiente': pagina_obj.has_next(),
        'tiene_anterior': pagina_obj.has_previous(),
    })


# ─── CREAR PUBLICACIÓN ────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_crear_publicacion(request):
    """
    POST /api/comunidad/crear/
    Crea una nueva publicación. Requiere: ruta_id, comentario, imagen (opcional).
    """
    from routes.models import Ruta

    ruta_id = request.data.get('ruta_id')
    comentario = request.data.get('comentario', '').strip()
    imagen = request.FILES.get('imagen')

    if not ruta_id:
        return Response({'error': 'Debes seleccionar una ruta.'}, status=400)
    if not comentario:
        return Response({'error': 'El comentario no puede estar vacío.'}, status=400)

    try:
        ruta = Ruta.objects.get(id=ruta_id)
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada.'}, status=404)

    publicacion = Publicacion.objects.create(
        usuario=request.user,
        ruta=ruta,
        comentario=comentario,
        imagen=imagen,
    )

    return Response({
        'id': publicacion.id,
        'usuario': publicacion.usuario.username,
        'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'ruta_id': ruta.id,
        'ruta_nombre': ruta.nombre_ruta,
        'comentario': publicacion.comentario,
        'imagen': request.build_absolute_uri(publicacion.imagen.url) if publicacion.imagen else None,
        'fecha': publicacion.fecha_publicacion.strftime('%d de %B de %Y · %H:%M'),
        'total_comentarios': 0,
    }, status=201)


# ─── ELIMINAR PUBLICACIÓN ─────────────────────────────────────────────────────
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_eliminar_publicacion(request, pub_id):
    """
    DELETE /api/comunidad/<id>/eliminar/
    Solo el dueño puede eliminar.
    """
    try:
        pub = Publicacion.objects.get(id=pub_id, usuario=request.user)
        pub.delete()
        return Response({'mensaje': 'Publicación eliminada.'})
    except Publicacion.DoesNotExist:
        return Response({'error': 'No encontrada o no tienes permiso.'}, status=404)


# ─── COMENTARIOS DE UNA PUBLICACIÓN ──────────────────────────────────────────
@api_view(['GET'])
@permission_classes([AllowAny])
def api_comentarios_publicacion(request, pub_id):
    """
    GET /api/comunidad/<id>/comentarios/
    """
    try:
        pub = Publicacion.objects.get(id=pub_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada.'}, status=404)

    comentarios = pub.comentarios.all().order_by('fecha').select_related('usuario')
    data = [{
        'id': c.id,
        'usuario': c.usuario.username,
        'nombre_completo': f"{c.usuario.first_name} {c.usuario.last_name}".strip() or c.usuario.username,
        'texto': c.texto,
        'fecha': c.fecha.strftime('%d/%m/%Y %H:%M'),
    } for c in comentarios]

    return Response({'comentarios': data})


# ─── CREAR COMENTARIO ─────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_crear_comentario_pub(request, pub_id):
    """
    POST /api/comunidad/<id>/comentarios/crear/
    """
    try:
        pub = Publicacion.objects.get(id=pub_id)
    except Publicacion.DoesNotExist:
        return Response({'error': 'Publicación no encontrada.'}, status=404)

    texto = request.data.get('texto', '').strip()
    if not texto:
        return Response({'error': 'El comentario no puede estar vacío.'}, status=400)

    comentario = Comentario.objects.create(
        publicacion=pub,
        usuario=request.user,
        texto=texto,
    )

    return Response({
        'id': comentario.id,
        'usuario': comentario.usuario.username,
        'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'texto': comentario.texto,
        'fecha': comentario.fecha.strftime('%d/%m/%Y %H:%M'),
    }, status=201)