# Generated by Django 5.1.7 on 2025-06-03 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0003_chatmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatgroup',
            name='is_personal_chat',
            field=models.BooleanField(default=False),
        ),
    ]
