# Generated by Django 2.2.6 on 2019-10-21 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_auto_20191021_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='public_key',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
