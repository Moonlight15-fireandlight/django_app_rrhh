# Generated by Django 4.1.1 on 2022-09-30 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="database",
            name="status",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterModelTable(name="database", table="Database",),
    ]
