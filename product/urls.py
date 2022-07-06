from django.urls import path
from . import views
#假如一个项目中有大量的应用，那就要用以命名空间，防止有相同的url分别不清
app_name = 'product' #模板中用： product:detail
urlpatterns = [
    path('product_post/',views.product_content_post,name='product_content_post'),
    path('seller_post/',views.seller_content_post,name='seller_content_post'),
]