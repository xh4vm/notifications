# Generated by Django 4.0.8 on 2023-01-02 08:24

import uuid

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL('create schema if not exists content;'),
        migrations.CreateModel(
            name='TypeEvent',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=255, verbose_name='Name')),
                ('template_file', models.FileField(upload_to='static/emails_template/')),
                ('template_params', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255), blank=True, size=None)),
            ],
            options={
                'verbose_name': 'Type_event',
                'verbose_name_plural': 'Type_event',
                'db_table': 'content"."type_event',
            },
        ),
        migrations.AddIndex(
            model_name='typeevent',
            index=models.Index(fields=['name'], name='type_event_name_0b64a5_idx'),
        ),
    ]
