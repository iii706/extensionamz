from django.contrib import admin
from django.utils.html import format_html
from product.models import Product,Rank,Review,SellerBase,SellerDetail

# Register your models here.

class GuardedAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/guarded_admin.js',)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','IMAGE','title','cat',"last_rank",'last_review_count','add_date_first_available','show_mod_time']
    list_display_links = ['id'] #可以直接链接到编辑页面
    list_filter = ['cat']
    search_fields = ["title","asin"]

    def IMAGE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><img src='{image}' width=150 ><br/></a>",asin=obj.asin, image=obj.image)

    IMAGE.short_description = "产品详情"






@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ['id','product','rank','show_add_time','show_mod_time']


@admin.register(SellerBase)
class SellerBaseAdmin(admin.ModelAdmin):
    list_display = ['id','seller_id','brand_name','country','last_product_counts','last_days_30_ratings','last_days_90_ratings','last_year_ratings','last_life_ratings','show_add_time','show_mod_time']
    list_filter = ['country','display']




@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['id','product','review_counts','show_add_time','show_mod_time']

@admin.register(SellerDetail)
class SellerDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'seller_base', 'product_counts', 'days_30_ratings', 'days_90_ratings', 'year_ratings', 'life_ratings', 'show_add_time', 'show_mod_time']
    list_display_links = ['seller_base']  # 可以直接链接到编辑页面






