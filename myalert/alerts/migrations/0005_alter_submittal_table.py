# Generated by Django 4.0.3 on 2022-04-14 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0004_alter_submittal_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittal',
            name='table',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]
