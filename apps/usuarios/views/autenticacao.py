from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from apps.usuarios.forms import LoginForm  # type: ignore


class CustomLoginView(LoginView):
    template_name = "usuarios/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
