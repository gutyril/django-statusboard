# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('occurred', models.DateTimeField(default=django.utils.timezone.now, verbose_name='occurred')),
                ('closed', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'incident',
                'verbose_name_plural': 'incidents',
            },
        ),
        migrations.CreateModel(
            name='IncidentUpdate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('status', models.IntegerField(verbose_name='status', choices=[(0, 'Investigating'), (1, 'Identified'), (2, 'Watching'), (3, 'Fixed')])),
                ('description', models.TextField(verbose_name='description')),
                ('incident', models.ForeignKey(related_query_name='update', related_name='updates', verbose_name='incident', to='statusboard.Incident')),
            ],
            options={
                'verbose_name': 'incident update',
                'verbose_name_plural': 'incident updates',
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('scheduled', models.DateTimeField(verbose_name='scheduled')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description')),
            ],
            options={
                'verbose_name': 'maintenance',
                'verbose_name_plural': 'maintenances',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('href', models.URLField(blank=True)),
                ('status', models.IntegerField(verbose_name='status', choices=[(0, 'Operational'), (1, 'Performance issues'), (2, 'Partial outage'), (3, 'Major outage')])),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='priority')),
            ],
            options={
                'verbose_name': 'service',
                'verbose_name_plural': 'services',
            },
        ),
        migrations.CreateModel(
            name='ServiceGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='name')),
                ('priority', models.PositiveIntegerField(default=0, verbose_name='priority')),
                ('collapse', models.IntegerField(default=0, choices=[(0, 'Never collapse'), (1, 'Always collapse'), (2, 'Collapse when all the services are operational')])),
            ],
            options={
                'verbose_name': 'service group',
                'verbose_name_plural': 'service groups',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='groups',
            field=models.ManyToManyField(related_query_name='service', related_name='services', verbose_name='groups', to='statusboard.ServiceGroup'),
        ),
        migrations.AddField(
            model_name='incident',
            name='services',
            field=models.ManyToManyField(related_query_name='incident', related_name='incidents', verbose_name='services', to='statusboard.Service', blank=True),
        ),
    ]
