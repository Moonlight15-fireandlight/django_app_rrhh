# Generated by Django 4.1.1 on 2022-10-26 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_alter_database_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="database",
            name="renovacion",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="main.event"
            ),
        ),
    ]
