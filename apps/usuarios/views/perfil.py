from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def meu_perfil(request):
    return render(
        request,
        "usuarios/meu_perfil.html",
    )
