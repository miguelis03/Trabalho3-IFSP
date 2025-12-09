from django.contrib import admin
from .models import Livro, Emprestimo

class LivroAdmin (admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'ano', 'isbn', 'status')

admin.site.register(Livro, LivroAdmin)

class EmprestimoAdmin (admin.ModelAdmin):
    list_display = ('data_retirada', 'data_previsao', 'data_devolucao', 'status', 'livro_fk', 'usuario_fk')

admin.site.register(Emprestimo, EmprestimoAdmin)