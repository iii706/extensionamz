from django.db import models
from django.contrib import admin
# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe

#产品信息表
class Product(models.Model):
    seller = models.ForeignKey('Seller', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题",max_length=200)
    image = models.CharField(max_length=500,default='')
    product_dimensions = models.CharField(verbose_name="尺寸",max_length=200,default='')
    weight = models.CharField(verbose_name="重量",max_length=50,default='')
    asin = models.CharField(verbose_name="ASIN",max_length=10,default='',unique = True,null=False) #'https://www.amazon/dp/asin'
    price = models.FloatField(verbose_name="价格")
    cat = models.CharField(verbose_name="类目",max_length=100,default='')
    review_counts = models.IntegerField(verbose_name="评论数",)
    ratings = models.FloatField(verbose_name="评分",default='5.0')
    date_first_available = models.DateField(verbose_name="上架日期",default='1990-01-01')
    add_time = models.DateField(auto_now_add=True,verbose_name="采集时间")

    def __str__(self):
        return self.title[:20]

    class Meta:
        indexes = [
            models.Index(fields=["asin"])
        ]



#排名信息表
class Rank(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rank = models.IntegerField(verbose_name="排名")
    add_time = models.DateField(auto_now_add=True, verbose_name="采集时间")
    class Meta:
        indexes = [
            models.Index(fields=["product"])
        ]

#卖家信息表
class Seller(models.Model):
    brand_name = models.CharField(verbose_name="品牌名称",max_length=200)
    seller_id = models.CharField(verbose_name="卖家id",max_length=200,unique = True,null=False)
    days_30_ratings = models.IntegerField(verbose_name="30天fd数")
    days_90_ratings = models.IntegerField(verbose_name="90天fd数")
    year_ratings = models.IntegerField(verbose_name="一年fd数")
    life_ratings = models.IntegerField(verbose_name="总fd数")
    business_name = models.CharField(verbose_name="公司名称",max_length=300)
    business_addr = models.CharField(verbose_name="公司地址",max_length=300)
    country = models.CharField(verbose_name="所在国家",max_length=10,default='')
    add_time = models.DateField(auto_now_add=True, verbose_name="采集时间")
    class Meta:
        indexes = [
            models.Index(fields=["seller_id"])
        ]

#评论信息表
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    review_counts = models.IntegerField(verbose_name="评论数",default=0)
    add_time = models.DateField(auto_now_add=True, verbose_name="采集时间")
    class Meta:
        indexes = [
            models.Index(fields=["product"])
        ]
