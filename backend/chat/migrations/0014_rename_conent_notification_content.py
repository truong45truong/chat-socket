# Generated by Django 4.2.3 on 2023-07-28 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_notification_user_email_chat_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='conent',
            new_name='content',
        ),
    ]
