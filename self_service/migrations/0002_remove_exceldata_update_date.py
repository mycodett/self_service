# Generated by Django 5.1.3 on 2024-11-09 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('self_service', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exceldata',
            name='update_date',
        ),
    ]
