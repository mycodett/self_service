# Generated by Django 5.1.3 on 2024-11-10 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_service', '0003_alter_exceldata_allocated_on_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('heading', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
