# Generated by Django 5.1.1 on 2024-10-06 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
