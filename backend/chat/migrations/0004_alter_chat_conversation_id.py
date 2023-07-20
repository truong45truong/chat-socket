# Generated by Django 4.1.4 on 2023-07-20 06:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_chat_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='conversation_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='conversions', to='chat.conversation'),
        ),
    ]
