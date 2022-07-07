from django.db import models
from django.contrib import admin
# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils import timezone



#产品信息表
class Product(models.Model):
    seller = models.ForeignKey('SellerBase', on_delete=models.CASCADE)
    title = models.CharField(verbose_name="标题",max_length=200)
    image = models.CharField(max_length=500,default='')
    product_dimensions = models.CharField(verbose_name="尺寸",max_length=200,default='')
    weight = models.CharField(verbose_name="重量",max_length=50,default='')
    asin = models.CharField(verbose_name="ASIN",max_length=10,default='',unique = True,null=False) #'https://www.amazon/dp/asin'
    price = models.FloatField(verbose_name="价格")
    last_rank = models.IntegerField(verbose_name="最新排名")
    last_review_count = models.IntegerField(verbose_name="最新评论数")
    cat = models.CharField(verbose_name="类目", max_length=100, default='')
    ratings = models.FloatField(verbose_name="评分",default='5.0')
    date_first_available = models.DateField(verbose_name="上架日期",default='1990-01-01')
    display = models.BooleanField(verbose_name="是否展示",default=True)
    add_time = models.DateTimeField("保存日期",default = timezone.now)
    mod_time = models.DateTimeField("最后修改日期",auto_now = True)

    def __str__(self):
        return self.title[:20]

    class Meta:
        indexes = [
            models.Index(fields=["asin"])
        ]

    def show_add_time(self):
        return self.add_time.strftime('%Y-%m-%d %H:%M:%S')

    show_add_time.admin_order_field = 'add_time'
    show_add_time.short_description = '抓取时间'

    def show_mod_time(self):
        return self.mod_time.strftime('%Y-%m-%d %H:%M:%S')

    show_mod_time.admin_order_field = 'add_time'
    show_mod_time.short_description = '最后修改时间'

    def save(self):
        super(Rank, self).save()
        self.number_of_orders = Rank.objects.all().order_by('mod_time')[0]
        self.customer.save()

#排名信息表
class Rank(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    rank = models.IntegerField(verbose_name="排名")
    add_time = models.DateTimeField("保存日期", default=timezone.now)
    mod_time = models.DateTimeField("最后修改日期", auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["product"])
        ]

    def show_add_time(self):
        return self.add_time.strftime('%Y-%m-%d %H:%M:%S')

    show_add_time.admin_order_field = 'add_time'
    show_add_time.short_description = '抓取时间'

    def show_mod_time(self):
        return self.mod_time.strftime('%Y-%m-%d %H:%M:%S')

    show_mod_time.admin_order_field = 'add_time'
    show_mod_time.short_description = '最后修改时间'


#卖家信息表
class SellerBase(models.Model):
    brand_name = models.CharField(verbose_name="品牌名称",max_length=200)
    seller_id = models.CharField(verbose_name="卖家id",max_length=200,unique = True,null=False)
    business_name = models.CharField(verbose_name="公司名称",max_length=300,default='')
    business_addr = models.CharField(verbose_name="公司地址",max_length=300,default='')
    country = models.CharField(verbose_name="所在国家",max_length=10,default='')
    display = models.BooleanField(verbose_name="是否跟踪", default=True)
    add_time = models.DateTimeField("保存日期", default=timezone.now)
    mod_time = models.DateTimeField("最后修改日期", auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["seller_id"])
        ]

    def show_add_time(self):
        return self.add_time.strftime('%Y-%m-%d %H:%M:%S')

    show_add_time.admin_order_field = 'add_time'
    show_add_time.short_description = '抓取时间'

    def show_mod_time(self):
        return self.mod_time.strftime('%Y-%m-%d %H:%M:%S')

    show_mod_time.admin_order_field = 'add_time'
    show_mod_time.short_description = '最后修改时间'


class SellerDetail(models.Model):
    seller_base = models.ForeignKey('SellerBase', on_delete=models.CASCADE)
    product_counts = models.IntegerField(verbose_name="产品数", default=0)
    days_30_ratings = models.IntegerField(verbose_name="30天fd数", default=0)
    days_90_ratings = models.IntegerField(verbose_name="90天fd数", default=0)
    year_ratings = models.IntegerField(verbose_name="一年fd数", default=0)
    life_ratings = models.IntegerField(verbose_name="总fd数", default=0)
    display = models.BooleanField(verbose_name="是否跟踪", default=True)
    add_time = models.DateTimeField("保存日期", default=timezone.now)
    mod_time = models.DateTimeField("最后修改日期", auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["seller_base"])
        ]

    def show_add_time(self):
        return self.add_time.strftime('%Y-%m-%d %H:%M:%S')

    show_add_time.admin_order_field = 'add_time'
    show_add_time.short_description = '抓取时间'

    def show_mod_time(self):
        return self.mod_time.strftime('%Y-%m-%d %H:%M:%S')

    show_mod_time.admin_order_field = 'add_time'
    show_mod_time.short_description = '最后修改时间'


#评论信息表
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    review_counts = models.IntegerField(verbose_name="评论数",default=0)
    add_time = models.DateTimeField("保存日期", default=timezone.now)
    mod_time = models.DateTimeField("最后修改日期", auto_now=True)
    class Meta:
        indexes = [
            models.Index(fields=["product"])
        ]
    def show_add_time(self):
        return self.add_time.strftime ('%Y-%m-%d %H:%M:%S')
    show_add_time.admin_order_field = 'add_time'
    show_add_time.short_description = '抓取时间'

    def show_mod_time(self):
        return self.mod_time.strftime ('%Y-%m-%d %H:%M:%S')
    show_mod_time.admin_order_field = 'add_time'
    show_mod_time.short_description = '最后修改时间'