# Generated by Django 5.1.1 on 2024-11-11 23:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_mensagem_is_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mensagens', to=settings.AUTH_USER_MODEL),
        ),
    ]