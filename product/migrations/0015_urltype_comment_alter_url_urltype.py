# Generated by Django 4.0.5 on 2022-07-15 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_alter_url_start_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='urltype',
            name='comment',
            field=models.CharField(default='', max_length=20, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='url',
            name='urltype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.urltype'),
        ),
    ]