from django.db import models
from django.contrib import admin
# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class Product(models.Model):
    title = models.CharField(verbose_name="标题",max_length=200)
    image = models.CharField(max_length=500,default='')
    product_dimensions = models.CharField(verbose_name="尺寸",max_length=200,default='')
    weight = models.CharField(verbose_name="重量",max_length=50,default='')
    asin = models.CharField(verbose_name="ASIN",max_length=10,default='',unique = True) #'https://www.amazon/dp/asin'
    price = models.FloatField(verbose_name="价格")
    cat = models.CharField(verbose_name="类目",max_length=100,default='')
    review_counts = models.IntegerField(verbose_name="评论数",)
    ratings = models.FloatField(verbose_name="评分",default='5.0')
    date_first_available = models.DateField(verbose_name="上架日期",default='1990-01-01')
    add_time = models.DateField(auto_now_add=True,verbose_name="采集时间")

    def __str__(self):
        return self.title[:20]




class Rank(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rank = models.IntegerField(verbose_name="排名")
    add_time = models.DateField(auto_now_add=True, verbose_name="采集时间")


        # return format_html(
        #     '<a href="{}">{}</a>',
        #     'www.baidu.com',
        #     "百度"
        # )
