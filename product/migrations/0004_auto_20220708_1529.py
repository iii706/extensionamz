# Generated by Django 3.2.13 on 2022-07-08 07:29

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_remove_product_review_counts_product_last_rank_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_content', models.CharField(max_length=200, verbose_name='关键词')),
                ('search_month_vol', models.IntegerField(default=0, verbose_name='月搜索量')),
                ('search_3m_vol', models.IntegerField(default=0, verbose_name='3月搜索量')),
                ('search_12m_vol', models.IntegerField(default=0, verbose_name='年均搜索量')),
                ('search_rank', models.IntegerField(default=9999999, verbose_name='词排名')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('mod_time', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
            ],
        ),
        migrations.CreateModel(
            name='WordShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_persent', models.FloatField(verbose_name='搜索占比')),
                ('add_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='保存日期')),
                ('mod_time', models.DateTimeField(auto_now=True, verbose_name='最后修改日期')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.word')),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
        ),
        migrations.AddField(
            model_name='word',
            name='product',
            field=models.ManyToManyField(through='product.WordShip', to='product.Product'),
        ),
        migrations.AddIndex(
            model_name='wordship',
            index=models.Index(fields=['word', 'product'], name='product_wor_word_id_968dd4_idx'),
        ),
        migrations.AddIndex(
            model_name='word',
            index=models.Index(fields=['word_content', 'search_rank'], name='product_wor_word_co_cc5d9c_idx'),
        ),
    ]
