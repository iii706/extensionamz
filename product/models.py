from django.db import models
from django.contrib import admin
# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=500,default='')
    product_dimensions = models.CharField(max_length=200,default='')
    weight = models.CharField(max_length=50,default='')
    asin = models.CharField(max_length=10,default='') #'https://www.amazon/dp/asin'
    price = models.FloatField()
    rank = models.IntegerField()
    cat = models.CharField(max_length=100,default='')
    review_counts = models.IntegerField()
    ratings = models.FloatField(default='5.0')
    date_first_available = models.DateField(default='1990-01-01')

    def __str__(self):
        return self.title[:20]



        # return format_html(
        #     '<a href="{}">{}</a>',
        #     'www.baidu.com',
        #     "百度"
        # )
