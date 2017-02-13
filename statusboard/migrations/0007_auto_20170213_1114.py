# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-02-13 11:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('statusboard', '0006_maintenance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incident',
            options={'verbose_name': 'incidente', 'verbose_name_plural': 'incidenti'},
        ),
        migrations.AlterModelOptions(
            name='incidentupdate',
            options={'verbose_name': "aggiornamento dell'incidente", 'verbose_name_plural': "aggiornamenti dell'incidente"},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'verbose_name': 'manutenzione', 'verbose_name_plural': 'manutenzioni'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'verbose_name': 'servizio', 'verbose_name_plural': 'servizi'},
        ),
        migrations.AlterModelOptions(
            name='servicegroup',
            options={'verbose_name': 'gruppo dei servizi', 'verbose_name_plural': 'gruppi dei servizi'},
        ),
        migrations.AlterField(
            model_name='incident',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='occurred',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='avvenuto'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='statusboard.Service', verbose_name='servizio'),
        ),
        migrations.AlterField(
            model_name='incidentupdate',
            name='description',
            field=models.TextField(verbose_name='descrizione'),
        ),
        migrations.AlterField(
            model_name='incidentupdate',
            name='incident',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', related_query_name='update', to='statusboard.Incident', verbose_name='incidente'),
        ),
        migrations.AlterField(
            model_name='incidentupdate',
            name='status',
            field=models.IntegerField(choices=[(0, 'In studio'), (1, 'Identificato'), (2, 'In esame'), (3, 'Risolto')], verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='description',
            field=models.TextField(verbose_name='descrizione'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='name',
            field=models.CharField(max_length=255, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='scheduled',
            field=models.DateTimeField(verbose_name='pianificato'),
        ),
        migrations.AlterField(
            model_name='service',
            name='description',
            field=models.TextField(verbose_name='descrizione'),
        ),
        migrations.AlterField(
            model_name='service',
            name='groups',
            field=models.ManyToManyField(related_name='services', related_query_name='service', to='statusboard.ServiceGroup', verbose_name='gruppi'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='nome'),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.IntegerField(choices=[(0, 'Operativo'), (1, 'Problemi di performance'), (2, 'Interruzione parziale'), (3, 'Interruzione totale')], verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='servicegroup',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='nome'),
        ),
    ]
