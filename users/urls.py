from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from . import api_views
from . import admin_api_views

app_name = 'users'

urlpatterns = [
    # ============================
    # AUTENTICACIÓN (Django vistas)
    # ============================
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro_usuario, name='registro'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),

    # ============================
    # RECUPERACIÓN DE CONTRASEÑA
    # ============================
    path('password_reset/',
         auth_views.PasswordResetView.as_view(
             success_url=reverse_lazy('users:password_reset_done')
         ),
         name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth-forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='auth-forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='auth-forgot_password/password_reset_complete.html'), name='password_reset_complete'),

    # ============================
    # PERFIL DE USUARIO
    # ============================
    path('perfil_usuario/', views.perfil_usuario, name='perfil_usuario'),

    # ============================
    # VISTAS DE ADMINISTRADOR
    # ============================
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('estadisticas/', views.admin_estadisticas, name='admin_estadisticas'),
    path('rutas_admin/', views.admin_rutas, name='admin_rutas'),
    path('reportes/', views.admin_reportes, name='admin_reportes'),
    path('usuarios/', views.admin_usuarios, name='admin_usuarios'),

    # ============================
    # API REST - JWT (para React)
    # ============================
    path('api/auth/registro/', api_views.api_registro, name='api_registro'),
    path('api/auth/login/', api_views.api_login, name='api_login'),
    path('api/auth/logout/', api_views.api_logout, name='api_logout'),
    path('api/auth/perfil/', api_views.api_perfil, name='api_perfil'),
    path('api/auth/perfil/actualizar/', api_views.api_actualizar_perfil, name='api_actualizar_perfil'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ============================
    # API REST - ADMIN
    # ============================
    path('api/auth/usuarios/', api_views.api_lista_usuarios, name='api_lista_usuarios'),
    path('api/auth/usuarios/<int:user_id>/rol/', api_views.api_cambiar_rol, name='api_cambiar_rol'),

    path('api/admin/dashboard/', admin_api_views.api_admin_dashboard, name='api_admin_dashboard'),
    path('api/admin/usuarios/', admin_api_views.api_admin_usuarios, name='api_admin_usuarios'),
    path('api/admin/usuarios/<int:user_id>/rol/', admin_api_views.api_admin_cambiar_rol, name='api_admin_cambiar_rol'),
    path('api/admin/usuarios/<int:user_id>/eliminar/', admin_api_views.api_admin_eliminar_usuario, name='api_admin_eliminar_usuario'),
    path('api/admin/rutas/', admin_api_views.api_admin_rutas, name='api_admin_rutas'),
    path('api/admin/rutas/<int:ruta_id>/eliminar/', admin_api_views.api_admin_eliminar_ruta, name='api_admin_eliminar_ruta'), 
]