# Generated by Django 4.0.5 on 2022-07-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_remove_url_replace_pattern_url_page_replace_pattern_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='start_page',
            field=models.IntegerField(default=1, verbose_name='开始页数'),
        ),
    ]