
from django.urls import path
from catalog import views


urlpatterns = [
    path('get_user_input/',
         views.get_user_input,
         name='get_user_input'),

    path('<str:user_input>/matching-products/',
         views.products_list,
         name='products_list'),

    path('all_products/',
         views.all_products_list,
         name='all_products_list'),

    path('product/<int:product_pk>/',
         views.product_detail,
         name='product_detail'),

    path('product/<int:product_pk>/substitutes/',
         views.substitutes_list,
         name='substitutes_list'),

    path('favorite_save/product/<int:product_pk>/substitute/<int:substitute_pk>/',
         views.favorite_save,
         name='favorite_save'),
    
    
     path('search_product/',
         views.search_product,
         name='search_product'),
]
