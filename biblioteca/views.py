from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Livro, Emprestimo

@login_required(login_url='/auth/login')
def biblioteca (request):

    emprestimos = Emprestimo.objects.filter(usuario_fk=request.user).order_by('-data_retirada')

    return render(request, 'biblioteca.html', {
        'emprestimos': emprestimos
    })

@login_required(login_url='/auth/login')
def listar_livros (request): 
    queryString = request.GET.get('q')
    livros = Livro.objects.all()

    if queryString:
        livros = livros.filter(
            Q(titulo__icontains=queryString) |
            Q(ano__icontains=queryString)
        )

    return render(request, 'biblioteca/listar_livros.html', {'livros': livros})

@login_required(login_url='/auth/login')
def criar_emprestimo (request):
    livros_disponiveis = Livro.objects.filter(status=1)

    emprestimo_ativo = Emprestimo.objects.filter(usuario_fk=request.user, status=True).exists()

    if emprestimo_ativo:
        return render(request, 'biblioteca/criar_emprestimo.html', {
            'livros': livros_disponiveis,
            'show_modal': True
        })
    
    if request.method == 'POST':
        livro_id = request.POST.get('livro')
        livro = Livro.objects.get(id=livro_id)

        usuario = request.user

        emprestimo = Emprestimo.objects.create(
            livro_fk= livro, 
            usuario_fk = usuario, 
            data_retirada = timezone.now(),
            data_previsao = timezone.now() + timedelta(days=7), 
            status = True
        )

        livro.status = 0
        livro.save()

        return redirect('/biblioteca/livros')
    
    return render(request, 'biblioteca/criar_emprestimo.html', {
        'livros': livros_disponiveis
    })

@login_required(login_url='/auth/login')
def devolver_livro (request, id):
    emprestimo = Emprestimo.objects.get(id=id)

    emprestimo.data_devolucao = timezone.now()
    emprestimo.status = False
    emprestimo.save()

    emprestimo.livro_fk.status = True
    emprestimo.livro_fk.save() 

    return redirect('biblioteca:home')