from django.shortcuts import render, redirect
from django.http import Http404
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'global/home.html')


def register(request):
    register_form_data = request.session.get('form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'driver/pages/register.html', {'form': form})


def create(request):
    if not request.POST:
        raise Http404("Método não permitido.")

    POST = request.POST
    request.session['form_data'] = POST  # Inseguro contem senha
    form = RegisterForm(POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        del (request.session['form_data'])
        messages.success(request, "Usuário cadastrado com sucesso!")
        return redirect('driver:login')
    return redirect('driver:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'driver/pages/login.html', {'form': form})


def login_create(request):
    if not request.POST:
        raise Http404("Método não permitido.")

    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', '')
        )

        if authenticated_user:
            messages.success(request, "Você está logado")
            login(request, authenticated_user)
            if request.user.is_superuser:
                print("Super usuario")
                return render(request, 'global/home.html')
            else:
                print("Usuario comum")
            # return render(request, 'global/home.html')
                return render(request, 'tracker/pages/deliveries_available.html')
        else:
            messages.error(request, "Dados inválidos")
            return redirect('driver:login')

    messages.error(request, "Erro no formulario")
    return redirect('driver:login')


@login_required(login_url='driver:login', redirect_field_name='next')
def logout_view(request):
    # request.session.flush()
    logout(request)
    messages.success(request, "Você saiu da conta.")
    return redirect('driver:login')
