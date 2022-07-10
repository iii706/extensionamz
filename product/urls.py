from django.urls import path
from . import views
#假如一个项目中有大量的应用，那就要用以命名空间，防止有相同的url分别不清
app_name = 'product' #模板中用： product:detail
urlpatterns = [
    path('post/',views.product_content_post,name='detail'),
    path('get_url/',views.get_url,name='get_url'),
    path('add_url/',views.add_url,name='add_url'),
    path('del_url/',views.del_url,name='del_url'),
    path('get_start_url/',views.get_start_url,name='get_start_url'),

]