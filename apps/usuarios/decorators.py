from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect

from apps.usuarios.models import PerfilUsuario


def perfil_required(*perfis):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("login")

            try:
                perfil = request.user.perfil

            except PerfilUsuario.DoesNotExist:
                messages.error(request, "Seu usuário não possui um perfil cadastrado.")

                return redirect("home")

            if perfil.perfil not in perfis:
                messages.error(
                    request, "Você não possui permissão para acessar esta página."
                )

                return redirect("home")

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator
