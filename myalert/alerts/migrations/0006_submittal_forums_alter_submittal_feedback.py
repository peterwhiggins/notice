# Generated by Django 4.0.3 on 2022-04-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0005_alter_submittal_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='submittal',
            name='forums',
            field=models.CharField(blank=True, default=' ', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='submittal',
            name='feedback',
            field=models.CharField(blank=True, default=' ', max_length=500, null=True),
        ),
    ]