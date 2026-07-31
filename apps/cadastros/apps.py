from django.apps import AppConfig


class CadastrosConfig(AppConfig):
    name = "apps.cadastros"

    def ready(self):
        import apps.cadastros.admin  # noqa: F401  # type: ignore
