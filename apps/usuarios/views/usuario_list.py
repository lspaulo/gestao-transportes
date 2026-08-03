from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def usuario_list(request):

    usuarios = User.objects.select_related("perfil").order_by("username")

    context = {
        "usuarios": usuarios,
    }

    return render(
        request,
        "usuarios/usuario_list.html",
        context,
    )
