from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.usuarios.models import PerfilUsuario, Setor


class PerfilUsuarioTests(TestCase):
    def setUp(self):
        self.trafego = Setor.objects.get(nome="Tráfego")
        self.logistica = Setor.objects.get(nome="Logística")

        User = get_user_model()
        self.usuario = User.objects.create_user(
            username="operador.trafego",
            email="operador@exemplo.com",
            password="senha-segura-teste",
        )

    def test_setores_iniciais_estao_disponiveis(self):
        nomes = set(Setor.objects.values_list("nome", flat=True))

        self.assertIn("Tráfego", nomes)
        self.assertIn("Logística", nomes)

    def test_usuario_possui_um_perfil_com_setor(self):
        perfil = PerfilUsuario.objects.create(
            usuario=self.usuario,
            setor=self.trafego,
        )

        self.assertEqual(self.usuario.perfil, perfil)  # type: ignore
        self.assertEqual(self.usuario.perfil.setor, self.trafego)  # type: ignore

    def test_usuario_nao_pode_ter_dois_perfis(self):
        PerfilUsuario.objects.create(
            usuario=self.usuario,
            setor=self.trafego,
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            PerfilUsuario.objects.create(
                usuario=self.usuario,
                setor=self.logistica,
            )
