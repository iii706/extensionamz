from django.contrib import admin
from django.utils.html import format_html
from product.models import Product,Rank,Review,Seller

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['IMAGE','title','cat','review_counts','date_first_available','ratings','add_time',"show_rank"]
    list_display_links = ['date_first_available'] #可以直接链接到编辑页面
    list_filter = ['cat']
    search_fields = ["title","asin"]

    def IMAGE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><img src='{image}' width=150 ><br/></a>",asin=obj.asin, image=obj.image)

    IMAGE.short_description = "产品详情"

    def show_rank(self,obj): #获取所有的rank
        return [i.rank for i in obj.rank_set.all()]

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['id','product','rank','add_time']


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['id','brand_name','days_30_ratings','days_90_ratings','year_ratings','life_ratings','business_addr','add_time']

@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','review_counts','add_time','add_time']








