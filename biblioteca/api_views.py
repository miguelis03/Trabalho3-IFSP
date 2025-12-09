# biblioteca/api_views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import DevolucaoSerializer

class DevolucaoViewSet(viewsets.ViewSet):
    """
    ViewSet para registrar devolução de livros.
    """

    def create(self, request):
        serializer = DevolucaoSerializer(data=request.data)
        if serializer.is_valid():
            emprestimo = serializer.save()
            return Response({
                "mensagem": "Livro devolvido com sucesso!",
                "emprestimo_id": emprestimo.id,
                "livro": emprestimo.livro_fk.titulo,
                "data_devolucao": emprestimo.data_devolucao
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
