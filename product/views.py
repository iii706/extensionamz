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

def get_list_url(request):
    count = request.GET['count']
    url = Url.objects.all().order_by("mod_time")
    ret_urls = []
    if len(url) > 0:
        start_url = url[0].start_url
        url_id = url[0].id
        start_page = url[0].start_page
        end_page = url[0].end_page
        current_page = start_page
        for page in range(start_page,end_page):
            ret_url = start_url.replace('<page>',str(page)).replace("<pre_page>",str(page-1))
            print(page,end_page,settings.REDIS_BL.cfExists(settings.LIST_URL_FILTER, ret_url),ret_url)
            if settings.REDIS_BL.cfExists(settings.LIST_URL_FILTER, ret_url) != 1:
                ret_urls.append(ret_url)
            if len(ret_urls) >= int(count):
                current_page = page
                break
        print(ret_urls)
        if len(ret_urls) == 0: ##已经抓取完了，看需不需要重新抓取？
            url[0].start_page = 1
            url[0].save()

        return HttpResponse(json.dumps({"msg":1,"urls": ret_urls,"url_id":url_id,'current_page':current_page}))
    else:
        return HttpResponse(json.dumps({"msg":0}))


#获取一条待爬取list链接
def get_asin_url(request):
    count = request.GET["count"]
    asins = []
    for i in range(int(count)):
        asin = settings.REDIS_CONN.srandmember(settings.DETAIL_URL_QUEUE)
        if asin and settings.REDIS_BL.cfExists(settings.DETSIL_URL_FILTER, asin) != 1:
            asins.append(asin.decode())
    if len(asins) > 0:
        return HttpResponse(json.dumps({"msg":1,"asins":asins}))
    else:
        return HttpResponse(json.dumps({"msg":0,"asins": ""}))

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
def add_asin_url(request):
    data = json.loads(request.body.decode("utf-8"))
    asins = data['asins']
    current_url = data['current_url']
    url_id = data['url_id']
    current_page = data['current_page']
    print(request,asins,current_url)
    if asins != '':
        asin_arr = [asin for asin in asins.split("|")]
        pipe = settings.REDIS_CONN.pipeline()
        for asin in asin_arr:
            pipe.sadd(settings.DETAIL_URL_QUEUE,asin)
        pipe.execute()
        settings.REDIS_BL.cfAddNX(settings.LIST_URL_FILTER,current_url)
    if url_id != "" and current_page != '':
        r = Url.objects.get(id=url_id)
        r.start_page = current_page
        r.save()
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