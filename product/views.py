from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from lxml import etree
import re
from datetime import datetime
from product.models import Product,SellerBase,Url
from django.utils import timezone
import redis
from django.conf import settings
import json

def get_start_url(request):
    url = Url.objects.all().order_by("mod_time")
    if len(url) > 0:
        start_url = url[0].start_url
        start_page = url[0].start_page
        end_page = url[0].end_page
        return HttpResponse(json.dumps({"msg":1,"start_url": start_url,'start_page':start_page,'end_page':end_page}))
    else:
        return HttpResponse(json.dumps({"msg":0}))





#获取一条待爬取list链接
def get_url(request):
    url_type = request.GET["url_type"]
    if url_type == "list":
        url = settings.REDIS_CONN.srandmember(settings.LIST_URL_QUEUE)
    elif url_type == 'asin':
        url = settings.REDIS_CONN.srandmember(settings.DETAIL_URL_QUEUE)
    if url:
        return HttpResponse(json.dumps({"url":url.decode()}))
    else:
        return HttpResponse(json.dumps({"url": ""}))
#删除一条待爬取list链接
def del_url(request):
    url_type = request.GET["url_type"]
    urls_str = request.GET['urls']
    print(urls_str)
    if urls_str == '':
        return HttpResponse(json.dumps({"msg":"0"}))
    else:
        if url_type == "list":
            key_str = settings.LIST_URL_QUEUE
        elif url_type == 'asin':
            key_str = settings.DETAIL_URL_QUEUE
            urls_str = urls_str
        settings.REDIS_CONN.srem(key_str,urls_str)
        return HttpResponse(json.dumps({"msg": "1"}))

##增加链接
def add_url(request):
    data = json.loads(request.body.decode("utf-8"))
    url_type = data['url_type']
    urls_str = data['urls']
    #print(request,urls_str)
    if urls_str == '':
        return HttpResponse(json.dumps({"msg":"0"}))
    else:
        if url_type == "list":
            key_str = settings.LIST_URL_QUEUE
            urls_split = urls_str.split("|")
        elif url_type == 'asin':
            key_str = settings.DETAIL_URL_QUEUE
            urls_split = [i for i in urls_str.split("|")]
        pipe = settings.REDIS_CONN.pipeline()
        for url in urls_split:
            pipe.sadd(key_str,url)
        pipe.execute()
        return HttpResponse(json.dumps({"msg":"1"}))



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