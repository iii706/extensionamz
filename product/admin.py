from django.contrib import admin
from django.utils.html import format_html
from product.models import Product,Rank,Review,SellerBase,SellerDetail

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['IMAGE','title','cat','date_first_available','ratings','show_add_time',"show_rank",'show_mod_time']
    list_display_links = ['date_first_available'] #可以直接链接到编辑页面
    list_filter = ['cat']
    search_fields = ["title","asin"]

    def IMAGE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><img src='{image}' width=150 ><br/></a>",asin=obj.asin, image=obj.image)

    IMAGE.short_description = "产品详情"

    def show_rank(self,obj): #获取所有的rank
        return obj.tutorialstats.rank

    show_rank.admin_order_field = 'product_rank'
    show_rank.short_description = '最新排名'

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['id','product','rank','show_add_time','show_mod_time']


@admin.register(SellerBase)
class SellerBaseAdmin(admin.ModelAdmin):
    list_display = ['id','seller_id','brand_name','country','show_add_time','show_mod_time','days_30_ratings']
    list_filter = ['country','display']

    def days_30_ratings(self,obj):
        ret = obj.sellerdetail_set.all().order_by("mod_time")
        if len(ret)>0:
            return ret[0].days_30_ratings
        else:
            return 0

    days_30_ratings.admin_order_field = 'sellerdetail'
    days_30_ratings.short_description = '30天fd数'


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','product','review_counts','show_add_time','show_mod_time']

@admin.register(SellerDetail)
class SellerDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller_base', 'product_counts', 'days_30_ratings', 'days_90_ratings', 'year_ratings', 'life_ratings', 'show_add_time', 'show_mod_time']
    list_display_links = ['seller_base']  # 可以直接链接到编辑页面






