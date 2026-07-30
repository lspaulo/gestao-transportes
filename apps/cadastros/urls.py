from django.urls import path

from . import views

app_name = "cadastros"

urlpatterns = [
    path(
        "funcionarios/",
        views.funcionario_list,
        name="funcionario_list",
    ),
    path(
        "funcionarios/novo/",
        views.funcionario_create,
        name="funcionario_create",
    ),
]
