# Generated by Django 5.1.2 on 2024-12-01 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='kakaoid',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
