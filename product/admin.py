from django.contrib import admin
from django.utils.html import format_html
from product.models import Product
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['IMAGE','TITLE','cat','rank','review_counts','date_first_available','ratings']
    list_display_links = ['date_first_available'] #可以直接链接到编辑页面

    def IMAGE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><img src='{image}' width=150 ><br/></a>",asin=obj.asin, image=obj.image)

    IMAGE.short_description = "产品详情"

    def CAT(self,obj):
        return format_html("<h3>{cat}</h3>", cat=obj.cat)

    CAT.short_description = "类目"

    def TITLE(self,obj):
        return format_html("<a href='https://www.amazon.com/dp/{asin}' target='blank'><h3>{title}</h3></a>", title=obj.title[:100],asin=obj.asin)

    TITLE.short_description = "标题"


    def RANK(self,obj):
        return format_html("<h3>{rank}<h3>", rank=obj.rank)

    RANK.short_description = "大类排名"

    def REVIEW_COUNTS(self,obj):
        return format_html("<h3>{review_counts}<h3>", review_counts=obj.review_counts)

    REVIEW_COUNTS.short_description = "评论数"


    def ADD_TIME(self,obj):
        return format_html("<h3>{date_first_available}<h3>", date_first_available=obj.date_first_available)

    ADD_TIME.short_description = "上架时间"







