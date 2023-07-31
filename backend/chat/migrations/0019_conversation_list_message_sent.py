# Generated by Django 4.2.3 on 2023-07-28 15:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0018_remove_conversation_is_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='list_message_sent',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), default=[], size=None),
            preserve_default=False,
        ),
    ]