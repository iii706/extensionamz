# Generated by Django 3.2.13 on 2022-07-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20220706_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='country',
            field=models.CharField(default='', max_length=10, verbose_name='所在国家'),
        ),
    ]
