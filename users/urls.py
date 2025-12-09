from django.urls import path, include 
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='cadastro'), 
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(next_page='/auth/login/'), name='logout'),
]