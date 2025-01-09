# Generated by Django 5.1.2 on 2024-12-02 13:02

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_user_kakaoid'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserKakao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kakao_id', models.UUIDField(db_column='kakaoId', default=uuid.uuid4, unique=True)),
                ('account_email', models.EmailField(db_column='accountEmail', max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(db_column='phoneNumber', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_column='createdAt')),
                ('deleted_at', models.DateTimeField(blank=True, db_column='deletedAt', null=True)),
            ],
            options={
                'db_table': 'UserKakao',
                'managed': False,
            },
        ),
    ]
