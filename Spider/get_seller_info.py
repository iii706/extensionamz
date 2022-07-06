import cloudscraper
from datetime import datetime
from lxml import etree
import os,sys
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取项目名的目录(因为我的当前文件是在项目名下的文件夹下的文件.所以是../)
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AmazonProductsScout.settings")

import django
django.setup()

from product.models import Seller
from django.utils import timezone
#print(datetime.now().strftime ('%Y-%m-%d %H:%M:%S'))

sellers = Seller.objects.all().order_by("mod_time")
for seller in sellers:
    seller_id = seller.seller_id
    print(seller_id)
    try:
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'linux',
                'desktop': True,

            }
        )
        start = datetime.now()
        #scraper = cloudscraper.create_scraper()
        page = scraper.get('https://www.amazon.com/sp?ie=UTF8&seller=%s&isAmazonFulfilled=1'%seller_id,timeout=5)
    except Exception as e:
        print(e)
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'linux',
                'desktop': True,

            }
        )
        start = datetime.now()
        # scraper = cloudscraper.create_scraper()
        page = scraper.get('https://www.amazon.com/sp?ie=UTF8&seller=%s&isAmazonFulfilled=1' % seller_id,timeout=20)
    print(page.status_code)

    selector = etree.HTML(page.text)
    title = selector.xpath("//title/text()")
    seller.brand_name = ''.join(selector.xpath('//*[@id="sellerName-rd"]/text()'))
    ratings_infos = selector.xpath('//table[@id="feedback-summary-table"]//tr[5]//td//text()')
    if len(ratings_infos) == 5:
        seller.days_30_ratings = ratings_infos[1].replace(",","")
        seller.days_90_ratings = ratings_infos[2].replace(",","")
        seller.year_ratings = ratings_infos[3].replace(",","")
        seller.life_ratings = ratings_infos[4].replace(",","")
    seller.business_name = ''.join(selector.xpath('//div[@id="page-section-detail-seller-info"]/div/div/div/div[2]/span[2]/text()'))
    seller.business_addr = "|".join(selector.xpath('//div[@class="a-row a-spacing-none indent-left"]//text()'))
    seller.country = seller.business_addr.split('|')[-1]
    #seller.add_time =
    print(seller.brand_name,ratings_infos,seller.business_name,seller.business_addr)
    seller.save()
    end = datetime.now()
    print('用时：',end-start,title)