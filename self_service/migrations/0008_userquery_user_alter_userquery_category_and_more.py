# Generated by Django 5.1.3 on 2024-11-18 11:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_service', '0007_remove_feedback_user_name_feedback_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userquery',
            name='user',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userquery',
            name='category',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='userquery',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
