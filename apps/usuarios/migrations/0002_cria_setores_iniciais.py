from django.db import migrations


def cria_setores_iniciais(apps, schema_editor):
    Setor = apps.get_model("usuarios", "Setor")

    for nome in ("Logística", "Tráfego"):
        Setor.objects.get_or_create(nome=nome)


class Migration(migrations.Migration):
    dependencies = [
        ("usuarios", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            cria_setores_iniciais,
            migrations.RunPython.noop,
        ),
    ]
