from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta
from django.db.models import Count

User = get_user_model()


def es_admin(user):
    return user.is_staff or user.is_superuser or getattr(user, 'rol', '') == 'admin'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_dashboard(request):
    """
    GET /api/admin/dashboard/
    Resumen general para el panel admin.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)

    from routes.models import Ruta
    from community.models import Publicacion

    total_usuarios = User.objects.count()
    usuarios_activos_hoy = User.objects.filter(last_login__date=now().date()).count()
    total_rutas = Ruta.objects.count()
    total_publicaciones = Publicacion.objects.count()

    # Usuarios activos últimos 7 días
    last_7 = [(now().date() - timedelta(days=i)) for i in range(6, -1, -1)]
    usuarios_por_dia = [
        {'fecha': d.strftime('%d/%m'), 'count': User.objects.filter(last_login__date=d).count()}
        for d in last_7
    ]

    # Top 5 rutas más vistas
    rutas_top = Ruta.objects.order_by('-vistas')[:5]
    rutas_data = [{'nombre': r.nombre_ruta, 'vistas': r.vistas} for r in rutas_top]

    # Usuarios por rol
    roles = {'usuario': 0, 'guia': 0, 'admin': 0}
    for u in User.objects.values('rol').annotate(count=Count('rol')):
        if u['rol'] in roles:
            roles[u['rol']] = u['count']

    return Response({
        'resumen': {
            'total_usuarios': total_usuarios,
            'usuarios_activos_hoy': usuarios_activos_hoy,
            'total_rutas': total_rutas,
            'total_publicaciones': total_publicaciones,
        },
        'usuarios_por_dia': usuarios_por_dia,
        'rutas_top': rutas_data,
        'roles': roles,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_usuarios(request):
    """
    GET /api/admin/usuarios/
    Lista todos los usuarios con info completa.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)

    usuarios = User.objects.all().order_by('-date_joined')
    data = [{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'rol': getattr(u, 'rol', 'usuario'),
        'is_staff': u.is_staff,
        'is_active': u.is_active,
        'date_joined': u.date_joined.strftime('%d/%m/%Y'),
        'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else None,
    } for u in usuarios]

    return Response({'usuarios': data, 'total': len(data)})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def api_admin_cambiar_rol(request, user_id):
    """
    PATCH /api/admin/usuarios/<id>/rol/
    Cambia el rol de un usuario.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)

    nuevo_rol = request.data.get('rol')
    if nuevo_rol not in ['usuario', 'guia', 'admin']:
        return Response({'error': 'Rol inválido.'}, status=400)

    try:
        usuario = User.objects.get(id=user_id)
        usuario.rol = nuevo_rol
        usuario.is_staff = (nuevo_rol == 'admin')
        usuario.save()
        return Response({'mensaje': f'Rol actualizado a {nuevo_rol}.', 'rol': nuevo_rol})
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_admin_eliminar_usuario(request, user_id):
    """
    DELETE /api/admin/usuarios/<id>/
    Elimina un usuario.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)
    if request.user.id == user_id:
        return Response({'error': 'No puedes eliminarte a ti mismo.'}, status=400)

    try:
        usuario = User.objects.get(id=user_id)
        usuario.delete()
        return Response({'mensaje': 'Usuario eliminado.'})
    except User.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_admin_rutas(request):
    """
    GET /api/admin/rutas/
    Lista todas las rutas con info completa.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)

    from routes.models import Ruta
    rutas = Ruta.objects.all().order_by('-fecha_creacion').select_related('creada_por')
    data = [{
        'id': r.id,
        'nombre_ruta': r.nombre_ruta,
        'dificultad': r.dificultad,
        'longitud': r.longitud,
        'duracion_estimada': str(r.duracion_estimada) if r.duracion_estimada else None,
        'ubicacion': r.ubicacion,
        'vistas': r.vistas,
        'creada_por': r.creada_por.username if r.creada_por else 'Sistema',
        'fecha_creacion': r.fecha_creacion.strftime('%d/%m/%Y') if r.fecha_creacion else None,
    } for r in rutas]

    return Response({'rutas': data, 'total': len(data)})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def api_admin_eliminar_ruta(request, ruta_id):
    """
    DELETE /api/admin/rutas/<id>/
    Elimina una ruta.
    """
    if not es_admin(request.user):
        return Response({'error': 'Sin permisos.'}, status=403)

    from routes.models import Ruta
    try:
        ruta = Ruta.objects.get(id=ruta_id)
        ruta.delete()
        return Response({'mensaje': 'Ruta eliminada.'})
    except Ruta.DoesNotExist:
        return Response({'error': 'Ruta no encontrada.'}, status=404)