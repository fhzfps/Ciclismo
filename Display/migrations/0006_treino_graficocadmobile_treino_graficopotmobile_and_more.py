# Generated by Django 4.0.4 on 2022-09-01 22:57

import Display.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Display', '0005_alter_treino_graficocad_alter_treino_graficopot_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='treino',
            name='GraficoCadMobile',
            field=models.FileField(blank=True, null=True, upload_to=Display.models.user_dir),
        ),
        migrations.AddField(
            model_name='treino',
            name='GraficoPotMobile',
            field=models.FileField(blank=True, null=True, upload_to=Display.models.user_dir),
        ),
        migrations.AddField(
            model_name='treino',
            name='GraficoZonasMobile',
            field=models.FileField(blank=True, null=True, upload_to=Display.models.user_dir),
        ),
    ]
