# Generated by Django 4.1.1 on 2022-10-30 17:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_event_comentario_rrhh_alter_event_comentario"),
    ]

    operations = [
        migrations.AlterModelTable(name="database", table="empleado",),
        migrations.AlterModelTable(name="empleados", table=None,),
    ]