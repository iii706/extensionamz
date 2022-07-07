from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from lxml import etree
import re
from datetime import datetime
from product.models import Product,SellerBase
from django.utils import timezone

def product_content_post(request):
    seller_id = request.GET["seller_id"]
    seller, b = SellerBase.objects.get_or_create(seller_id=seller_id)

    title = request.GET['title']
    image = request.GET['image']
    price = request.GET['price'].replace("$","").replace("US","")
    desc = request.GET['desc']
    asin = request.GET['asin']



    desc = desc.replace("\u200e",'')
    desc = desc.replace("\u200e",'')

    #print(desc)

    product_dimensions = '#NA'
    weight = '#NA'
    date_first_available = datetime.strptime("January 01, 1990", '%B %d, %Y')
    rank = 999999
    cat = '#NA'
    review_counts = 0
    ratings = 0

    items = desc.split("|")

    for item in items:

        if item.find('Package Dimensions') != -1:
            if item.find(';') != -1:
                product_dimensions = item.split(";")[0].replace("Package Dimensions",'').strip()
                weight = item.split(";")[1][1].strip()
            else:
                product_dimensions = item.replace("Package Dimensions",'').strip()
        if item.find('Item Weight') != -1:
            weight = item.replace('Item Weight','').strip()
        if item.find('Date First Available') != -1:
            date_first_available = item.replace("Date First Available",'').strip()
            date_first_available = datetime.strptime(date_first_available, '%B %d, %Y')
        if item.find('ASIN') != -1:
            asin = item.replace("ASIN",'').strip()
        if item.find('Best Sellers Rank') != -1:
            rank = item.replace("Best Sellers Rank","").split(' in ')[0].replace('#', '').replace(',', '').strip()
            cat = item.replace("Best Sellers Rank","").split(' in ')[-1].replace("(","").strip()
        if item.find('Customer Reviews') != -1:
            review_counts = item.replace("Customer Reviews","").split('out of 5 stars')[-1].replace("ratings","").replace("rating","").replace(',', '').strip()
            ratings = item.replace("Customer Reviews","").split('out of 5 stars')[0].strip()

    if review_counts == '':
        review_counts = 0
    if ratings == '':
        ratings = 0

    if rank == '':
        rank = 999999

    print(desc)
    print([product_dimensions, weight, date_first_available, asin, rank,cat, review_counts, ratings])

    defaults = {
        'seller':seller,
        'title':title,
        'price':price,
        'image':image,
        'product_dimensions':product_dimensions,
        'weight':weight,
        'date_first_available':date_first_available,
        'last_rank':rank,
        'last_review_count':review_counts,
        'ratings':ratings,
        'cat':cat,

    }
    if cat != "#NA":
        p,b = Product.objects.get_or_create(asin=asin,defaults=defaults)
        print("查找结果：",p,b)
        if b == False:
            day = (timezone.now() - p.mod_time).days
            print(asin,p.mod_time,day)
            if day >= 1:
                p2,b2 = Product.objects.update_or_create(defaults=defaults,asin=asin)
                print("更新结果：",b2)


    return HttpResponse({'mes':'1'})