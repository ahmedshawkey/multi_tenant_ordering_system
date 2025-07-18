from django.urls import path
from .views import product_list_create, get_product_detail, delete_product
from .views import order_list_create, get_order_detail
from .views import edit_order
from .views import mark_order_shipped

urlpatterns = [
    path('api/products/', product_list_create, name='product-list-create'),
    path('api/products/<int:pk>/', delete_product, name='delete-product'),
    path('api/products/<int:pk>/detail/', get_product_detail, name='product-detail'),
    path('api/orders/', order_list_create, name='order-list-create'),
    path('api/orders/<int:pk>/detail/', get_order_detail, name='order-detail'),
    path('api/orders/<int:pk>/edit/', edit_order, name='edit-order'),
    path('api/orders/<int:pk>/ship/', mark_order_shipped, name='mark-order-shipped'),

]
