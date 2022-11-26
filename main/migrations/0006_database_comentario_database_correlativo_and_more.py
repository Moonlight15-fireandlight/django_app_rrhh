# Generated by Django 4.1.1 on 2022-10-24 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_event"),
    ]

    operations = [
        migrations.AddField(
            model_name="database",
            name="comentario",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="database",
            name="correlativo",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="database",
            name="modalidad",
            field=models.CharField(
                blank=True,
                choices=[
                    ("QUINTA CATEGORIA", "Quinta Categoria"),
                    ("RECIBO POR HONORARIOS", "Recibo por honorarios"),
                    ("PRACTICAS PRE PROFESIONALES", "Practicas pre profesionales"),
                    ("PRACTICAS PROFESIONALES", "Practicas profesionales"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="database",
            name="motivo_cese",
            field=models.CharField(
                blank=True,
                choices=[
                    ("PERIODO DE PRUEBA", "Periodo de prueba"),
                    (
                        "TERMINO DE CONTRATO A SOLICITUD DEL JEFE INMEDIATO",
                        "Termino de contrato a solicitud del jefe inmediato",
                    ),
                    (
                        "TERMINO DE CONTRATO A SOLICITUD DEL COLABORADOR",
                        "Termino de contrato a solicitu del colaborador",
                    ),
                    ("RENUNCIA", "Renuncia"),
                    ("MUTUO DISENSO", "Mutuo disenso"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="database",
            name="plazo_renovacion",
            field=models.CharField(
                blank=True,
                choices=[
                    ("1 MES", "1 mes"),
                    ("2 MESES", "2 meses"),
                    ("3 MESES", "3 meses"),
                    ("4 MESES", "4 meses"),
                    ("5 MESES", "5 meses"),
                    ("6 MESES", "6 meses"),
                    ("12 MESES", "12 meses"),
                    ("NO RENOVADO", "No renovar"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AlterModelTable(name="database", table=None,),
    ]
