# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name=b'Name')),
                ('description', models.TextField(verbose_name=b'Description')),
                ('funding_goal', models.DecimalField(verbose_name=b'Funding Goal', max_digits=19, decimal_places=2)),
                ('current_funds', models.DecimalField(verbose_name=b'Current Funds', max_digits=19, decimal_places=2)),
                ('initiator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
