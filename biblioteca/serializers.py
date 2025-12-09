from rest_framework import serializers
from .models import Livro, Emprestimo
from django.utils import timezone

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = '__all__'

class EmprestimoSerializer(serializers.ModelSerializer):
    emprestimo_id = serializers.IntegerField(source='id', read_only=True)
    status = serializers.BooleanField(read_only=True)
    class Meta:
        model = Emprestimo
        fields = ['emprestimo_id','usuario_fk', 'livro_fk', 'data_retirada', 'status']
        
    def validate(self, attrs):
        livro = attrs.get('livro_fk')

        # Verifica se já existe empréstimo desse livro sem data_devolucao
        emprestimo_em_aberto = Emprestimo.objects.filter(
            livro_fk=livro,
            data_devolucao__isnull=True
        ).exists()
        print (emprestimo_em_aberto)
        if emprestimo_em_aberto:
            raise serializers.ValidationError(
                f"O livro '{livro}' já está emprestado e não foi devolvido."
            )

        return attrs
    
    def create(self, validated_data):
        # Cria o empréstimo
        emprestimo = Emprestimo.objects.create(**validated_data)

        # Atualiza o status do livro para 0 (emprestado)
        livro = validated_data['livro_fk']
        livro.status = 0
        livro.save()

        return emprestimo

class DevolucaoSerializer(serializers.Serializer):
    emprestimo_id = serializers.IntegerField()

    def validate(self, attrs):
        emprestimo_id = attrs.get("emprestimo_id")

        try:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        except Emprestimo.DoesNotExist:
            raise serializers.ValidationError("Empréstimo não encontrado.")

        if emprestimo.data_devolucao is not None:
            raise serializers.ValidationError("Este empréstimo já foi devolvido.")

        attrs["emprestimo"] = emprestimo
        return attrs

    def save(self):
        emprestimo = self.validated_data["emprestimo"]

        emprestimo.data_devolucao = timezone.now()
        emprestimo.status = False
        emprestimo.save()

        livro = emprestimo.livro_fk
        livro.status = True
        livro.save()

        return emprestimo
