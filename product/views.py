from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from lxml import etree
import re
from datetime import datetime
from product.models import Product,Rank,Review,SellerBase


def product_content_post(request):
    seller_id = request.GET["seller_id"]
    seller, b = SellerBase.objects.get_or_create(seller_id=seller_id)



    title = request.GET['title']
    image = request.GET['image']
    price = request.GET['price'].replace("$","").replace("US","")

    desc = request.GET['desc']

    desc = desc.replace("\u200e",'')
    desc = desc.replace("\u200e",'')

    #print(desc)

    product_dimensions = '#NA'
    weight = '#NA'
    date_first_available = datetime.strptime("January 01, 1990", '%B %d, %Y')
    asin = '#NA'
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

    if asin == '':
        asin = request.GET['asin']
    print(desc)
    print([product_dimensions, weight, date_first_available, asin, rank,cat, review_counts, ratings])

    p = Product()
    p.seller = seller
    p.title = title
    p.asin = asin
    p.price = price
    p.image = image
    p.product_dimensions = product_dimensions
    p.weight = weight
    p.date_first_available = date_first_available

    p.cat = cat
    p.review_counts = review_counts
    p.ratings = ratings
    if cat != "#NA":

        p.save()
        r = Rank()
        r.product = p
        r.rank = rank
        r.save()

        review = Review()
        review.review_counts = review_counts
        review.product = p
        review.save()

    print([asin,title[:50],price,image])
    return HttpResponse({'mes':'1'})