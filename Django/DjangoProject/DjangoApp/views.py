from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpRequest, HttpResponse
# Create your views here.

def menu_view(request: HttpRequest) -> HttpResponse:
    """
        Отображает главную страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной главной страницей.
    """
    return render(request, 'menu.html')

def homenotes_view(request: HttpRequest) -> HttpResponse:
    """
        Отображает главную страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной главной страницей.
    """
    return render(request, 'homenotes.html')

def register(request: HttpRequest) -> HttpResponse:
    """
        Регистрация нового пользователя.

        Если пользователь уже авторизован, происходит перенаправление
        на домашнюю страницу. В противном случае отображается форма
        регистрации, и, при успешной отправке формы, пользователь
        авторизуется и перенаправляется на домашнюю страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей регистрации.
    """
    if request.user.is_authenticated:
        return redirect('homenotes')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homenotes')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request: HttpRequest) -> HttpResponse:
    """
        Вход пользователя на сайт.

        Если пользователь уже авторизован, происходит перенаправление
        на домашнюю страницу. В противном случае отображается форма
        входа, и, при успешной отправке формы, пользователь авторизуется
        и перенаправляется на домашнюю страницу.

        Параметры:
            request (HttpRequest): Объект HTTP-запроса.

        Возвращает:
            HttpResponse: Ответ с отрисованной страницей входа.
    """
    if request.user.is_authenticated:
        return redirect('homenotes')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = request.POST.get('remember_me')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                if remember_me:
                    request.session.set_expiry(None)  # Сессия будет действительна до выхода
                else:
                    request.session.set_expiry(0)  # Сеанс завершится при закрытии браузера

                return redirect('homenotes')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
