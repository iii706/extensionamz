# Generated by Django 4.0.5 on 2022-07-15 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_urltype_url_url_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='url_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='product.urltype'),
        ),
    ]