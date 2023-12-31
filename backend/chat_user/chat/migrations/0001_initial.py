# Generated by Django 4.2.3 on 2023-08-07 09:04

import chat_base.core.constants.related_name
import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
            ],
            options={
                'verbose_name_plural': 'chats',
                'db_table': 'chats',
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_last', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('list_user_seen', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('list_message_sent', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('user_chat', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'conversations',
                'db_table': 'conversations',
            },
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'groupchats',
                'db_table': 'groupchats',
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('is_manager', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'members',
                'db_table': 'members',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('email_user_chat', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=10)),
                ('is_seem', models.BooleanField()),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('conversation_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name=chat_base.core.constants.related_name.RelatedName['NOTIFICATION_CONVERSATION'], to='chat.conversation')),
            ],
            options={
                'verbose_name_plural': 'notifications',
                'db_table': 'notifications',
            },
        ),
    ]
