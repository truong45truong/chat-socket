# Generated by Django 4.1.4 on 2023-07-20 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_remove_conversation_user_send'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='is_sent',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
