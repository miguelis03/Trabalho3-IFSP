from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Livro, Emprestimo
from .serializers import LivroSerializer, EmprestimoSerializer

class LivroViewSet(viewsets.ModelViewSet):
    queryset = Livro.objects.all()
    serializer_class = LivroSerializer

class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    @action(detail=True, methods=['post'])
    def devolucao(self, request, pk=None):
        emprestimo = self.get_object()

        if emprestimo.data_devolucao is not None:
            return Response({"erro": "Livro já devolvido"}, status=status.HTTP_400_BAD_REQUEST)

        # Atualiza datas e status
        emprestimo.data_devolucao = timezone.now()
        emprestimo.status = False
        emprestimo.livro_fk.status = True
        emprestimo.livro_fk.save()
        emprestimo.save()

        return Response({
            "mensagem": "Livro devolvido com sucesso!",
            "emprestimo_id": emprestimo.id,
            "livro": emprestimo.livro_fk.titulo,
            "data_devolucao": emprestimo.data_devolucao
        }, status=status.HTTP_200_OK)
