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
    urls = Url.objects.all().order_by("id")
    ret_urls = []
    if len(urls) > 0:
        for url in urls:
            if url.start_page < url.end_page:
                start_url = url.start_url
                url_id = url.id
                start_page = url.start_page
                end_page = url.end_page
                for page in range(start_page,end_page+1):
                    ret_url = start_url.replace('<page>',str(page)).replace("<pre_page>",str(page-1))
                    #print(page,end_page,settings.REDIS_BL.cfExists(settings.LIST_URL_FILTER, ret_url),ret_url)
                    if settings.REDIS_BL.cfExists(settings.LIST_URL_FILTER, ret_url) != 1:
                        ret_urls.append({"url":ret_url,"current_page":page})
                    if len(ret_urls) >= int(count):
                        break

                #print(url.id,ret_urls)
                return HttpResponse(
                    json.dumps({"msg": 1, "urls": ret_urls, "url_id": url_id}))
            elif (timezone.now() - url.add_time).days >= 3:
                ##已经抓取完了，看需不需要重新抓取？
                url.start_page = 1
                url.add_time = timezone.now() #更新保存的时间
                url.save()
                settings.REDIS_BL.delete(settings.LIST_URL_FILTER)
                return HttpResponse(json.dumps({"msg": 2})) #需要采集器刷新
    return HttpResponse(json.dumps({"msg":0}))



#获取一条待爬取list链接
#/product/get_asin_url/?count=8  #获取正常产品监控的asins
#/product/get_asin_url/?count=8&seller=1  #获取卖家id的asins来抓取，这个过滤器不会删除的

def get_asin_url(request):
    count = request.GET["count"]
    default_queue = settings.DETAIL_URL_QUEUE
    try:
        seller = request.GET["seller"]  #如果有传seller参数=1，则是抓取卖家id的asin
        if seller == "1":
            default_queue = settings.SELLER_URL_QUEUE
    except Exception as e:
        print(e)

    asins_ret = settings.REDIS_CONN.srandmember(default_queue,number=int(count))
    print(asins_ret)
    if len(asins_ret) > 0:
        return HttpResponse(json.dumps({"msg":1,"asins":[i.decode() for i in asins_ret]}))
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
    #print(request,asins,current_url)
    if asins != '':
        asin_arr = [asin for asin in asins.split("|")]
        #print(asin_arr)
        #加入抓取卖家id的asin队列，先过滤再加入
        ex_rets = settings.REDIS_BL.bfMExists(settings.SELLER_ASIN_FILTER, *(i for i in asin_arr))
        noex_asins = []
        for item in zip(ex_rets,asin_arr):
            if item[0] == 0:
                noex_asins.append(item[1])
        #print("noex_asins",noex_asins)
        pipe = settings.REDIS_CONN.pipeline()
        for asin in noex_asins:
            pipe.sadd(settings.SELLER_URL_QUEUE, asin)
        pipe.execute()

        #加入监控asin或符合队列
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
    data = json.loads(request.body.decode("utf-8"))
    data_ret = data['ret']
    asin = data['asin']
    if data_ret == 2:  #404的asin返回
        settings.REDIS_BL.cfAddNX(settings.DETSIL_URL_FILTER, asin)
        settings.REDIS_CONN.srem(settings.DETAIL_URL_QUEUE, asin)
        return HttpResponse(json.dumps({"msg": 0}))

    if data_ret == 3200: #只抓取卖家id:
        seller_id = data["seller_id"]
        seller, b = SellerBase.objects.get_or_create(seller_id=seller_id)
        settings.REDIS_BL.bfMAdd(settings.SELLER_ASIN_FILTER, asin)
        settings.REDIS_CONN.srem(settings.SELLER_URL_QUEUE, asin)
        return HttpResponse(json.dumps({"msg": 1,'ret':3200}))

    if data_ret == 3404: #抓取卖家id出现404
        settings.REDIS_BL.bfMAdd(settings.SELLER_ASIN_FILTER, asin)
        settings.REDIS_CONN.srem(settings.SELLER_URL_QUEUE, asin)
        return HttpResponse(json.dumps({"msg": 0, 'ret': 3404}))

    #print("asin",asin)

    seller_id = data["seller_id"]
    seller, b = SellerBase.objects.get_or_create(seller_id=seller_id)
    title = data['title']
    image = data['image']
    price = data['price'].replace("$","").replace("US","")
    desc = data['desc']




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
            review_counts = item.replace("Customer Reviews","").split('out of 5 stars')[-1].replace("ratings","").replace("rating","").replace("Reviews","").replace("Review","").replace(',', '').strip()
            ratings = item.replace("Customer Reviews","").split('out of 5 stars')[0].strip()

    if review_counts == '':
        review_counts = 0
    if ratings == '':
        ratings = 0

    if rank == '':
        rank = 999999

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
    asin = data['asin']
    #print('asin2:',asin)
    if asin != "": #ret为0，1都要删除asin的key
        settings.REDIS_BL.cfAddNX(settings.DETSIL_URL_FILTER, asin)
        settings.REDIS_CONN.srem(settings.DETAIL_URL_QUEUE, asin)

    if cat != "#NA" and data_ret == 1:
        p,b = Product.objects.get_or_create(asin=asin,defaults=defaults)
        print("查找结果：",p,b)
        if b == False:
            day = (timezone.now() - p.mod_time).days
            print(asin,p.mod_time,day)
            if day >= 1:
                p2,b2 = Product.objects.update_or_create(defaults=defaults,asin=asin)
                print("更新结果：",b2)

        return HttpResponse(json.dumps({"msg":1}))
    else:
        return HttpResponse(json.dumps({"msg":0}))