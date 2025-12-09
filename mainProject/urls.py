from django.contrib import admin
from django.urls import path, include
from . import views
from biblioteca.api_views import DevolucaoViewSet

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from biblioteca.api import LivroViewSet, EmprestimoViewSet
from users.api import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'livros', LivroViewSet)
router.register(r'emprestimos', EmprestimoViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'devolucao', DevolucaoViewSet, basename='devolucao')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  #  Endpoints REST
    path('', views.home, name='home'), 
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')), 
    path('biblioteca/', include('biblioteca.urls')),
]
