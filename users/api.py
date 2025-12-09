from rest_framework import viewsets
#from .models import Usuario
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
