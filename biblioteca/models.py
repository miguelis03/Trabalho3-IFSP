from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Livro (models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=100)
    ano = models.PositiveBigIntegerField()
    isbn = models.CharField(max_length=55)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo
    
class Emprestimo (models.Model):
    data_retirada = models.DateTimeField(auto_now_add=True)
    data_previsao = models.DateTimeField(editable=False)
    data_devolucao = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=True)

    livro_fk = models.ForeignKey(Livro, on_delete=models.CASCADE)
    usuario_fk = models.ForeignKey(User, on_delete=models.CASCADE)

    def save (self, *args, **kwargs):
        if not self.id:
            self.data_previsao = timezone.now() + timedelta(days=7)

        super().save(*args, **kwargs)

        def __str__(self):
            return f"Empréstimo de {self.usuario_fk.username} - {self.livro_fk.titulo}"