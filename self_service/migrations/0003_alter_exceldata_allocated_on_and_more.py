# Generated by Django 5.1.3 on 2024-11-09 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('self_service', '0002_remove_exceldata_update_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exceldata',
            name='allocated_on',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='exceldata',
            name='from_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='exceldata',
            name='uploaded_on',
            field=models.DateField(null=True),
        ),
    ]
