
from django.urls import path
from catalog import views


urlpatterns = [
    path('products/',
         views.products_list,
         name='products_list'),

    path('product/<int:product_pk>/',
         views.product_detail,
         name='product_detail'),

    path('product/<int:product_pk>/substitutes/',
         views.substitutes_list,
         name='substitutes_list'),

    path('favorite_save/product/<int:product_pk>/substitute/<int:substitute_pk>/',
         views.favorite_save,
         name='favorite_save'),
]
