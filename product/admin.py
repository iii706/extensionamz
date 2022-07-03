from django.contrib import admin
from django.utils.html import format_html
from product.models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['IMAGE','title','cat','rank','review_counts','date_first_available','ratings']
    list_display_links = ['date_first_available'] #可以直接链接到编辑页面
    list_filter = ['cat']
    search_fields = ["title","asin"]

    def IMAGE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><img src='{image}' width=150 ><br/></a>",asin=obj.asin, image=obj.image)

    IMAGE.short_description = "产品详情"









