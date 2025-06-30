"""
URL configuration for sistema_historias project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include # Asegúrate de importar include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("historias/", include("gestion_historias.urls")),

    # URLs de autenticación de Django
    path('accounts/login/', auth_views.LoginView.as_view(template_name='gestion_historias/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    # No necesitamos registro de usuarios por ahora, se crearán desde el admin.
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Redirigir la raíz del sitio a la lista de historias si el usuario está autenticado, o a login si no.
    # Esto se puede manejar mejor en una vista o con middleware, pero una redirección simple puede servir por ahora.
    # O simplemente, la página de inicio puede ser la lista de historias, protegida por @login_required en su vista.
    # Por ahora, dejaremos que el usuario navegue a /historias/listar/ o /accounts/login/ manualmente.
    # path('', RedirectView.as_view(url='/historias/listar/', permanent=False), name='index'),
    path("", RedirectView.as_view(pattern_name='listar_historias_clinicas', permanent=False), name='index_redirect'),


]
