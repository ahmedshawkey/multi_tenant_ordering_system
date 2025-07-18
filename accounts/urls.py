from django.urls import path
from .views import product_list_create, get_product_detail, delete_product
from .views import order_list_create, get_order_detail

urlpatterns = [
    path('api/products/', product_list_create, name='product-list-create'),
    path('api/products/<int:pk>/', delete_product, name='delete-product'),
    path('api/products/<int:pk>/detail/', get_product_detail, name='product-detail'),
    path('api/orders/', order_list_create, name='order-list-create'),
    path('api/orders/<int:pk>/detail/', get_order_detail, name='order-detail'),

]
