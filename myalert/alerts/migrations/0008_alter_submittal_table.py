# Generated by Django 4.0.3 on 2022-04-24 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0007_alter_submittal_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittal',
            name='table',
            field=models.FileField(upload_to=''),
        ),
    ]
