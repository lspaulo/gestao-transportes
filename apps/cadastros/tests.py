from django.test import TestCase
from django.urls import reverse

from apps.cadastros.models import ClasseOperacional


class ClasseOperacionalViewsTests(TestCase):
    def setUp(self):
        self.classe_ativa = ClasseOperacional.objects.create(
            nome="Cavalo Mecânico",
            descricao="Veículo trator.",
            possui_placa=True,
            ordem=1,
        )
        self.classe_inativa = ClasseOperacional.objects.create(
            nome="Carreta Desativada",
            possui_placa=True,
            ordem=2,
            ativo=False,
        )

    def test_listagem_mostra_apenas_classes_ativas_por_padrao(self):
        response = self.client.get(reverse("cadastros:classe_operacional_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.classe_ativa.nome)
        self.assertNotContains(response, self.classe_inativa.nome)

    def test_listagem_filtra_classes_inativas(self):
        response = self.client.get(
            reverse("cadastros:classe_operacional_list"),
            {"status": "inativos"},
        )

        self.assertContains(response, self.classe_inativa.nome)
        self.assertNotContains(response, self.classe_ativa.nome)

    def test_cria_classe_operacional(self):
        response = self.client.post(
            reverse("cadastros:classe_operacional_create"),
            {
                "nome": "Carreta Sider",
                "descricao": "Semirreboque com lonas laterais.",
                "possui_placa": "on",
                "ordem": 3,
                "ativo": "on",
            },
        )

        self.assertRedirects(response, reverse("cadastros:classe_operacional_list"))
        self.assertTrue(ClasseOperacional.objects.filter(nome="Carreta Sider").exists())

    def test_nao_permite_nome_de_classe_duplicado(self):
        response = self.client.post(
            reverse("cadastros:classe_operacional_create"),
            {
                "nome": self.classe_ativa.nome,
                "descricao": "",
                "ordem": 1,
                "ativo": "on",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ClasseOperacional.objects.filter(nome=self.classe_ativa.nome).count(), 1)
        self.assertIn("nome", response.context["form"].errors)

    def test_edita_classe_operacional(self):
        response = self.client.post(
            reverse(
                "cadastros:classe_operacional_update",
                args=[self.classe_ativa.pk],
            ),
            {
                "nome": "Cavalo Mecânico 6x2",
                "descricao": "Veículo trator atualizado.",
                "possui_placa": "on",
                "ordem": 5,
                "ativo": "on",
            },
        )

        self.assertRedirects(response, reverse("cadastros:classe_operacional_list"))
        self.classe_ativa.refresh_from_db()
        self.assertEqual(self.classe_ativa.nome, "Cavalo Mecânico 6x2")
        self.assertEqual(self.classe_ativa.ordem, 5)

    def test_altera_status_da_classe_operacional(self):
        response = self.client.get(
            reverse(
                "cadastros:classe_operacional_toggle_status",
                args=[self.classe_ativa.pk],
            )
        )

        self.assertRedirects(response, reverse("cadastros:classe_operacional_list"))
        self.classe_ativa.refresh_from_db()
        self.assertFalse(self.classe_ativa.ativo)
