from django.contrib import admin
from .models import Product
from .models import Order
import csv 
from django.http import HttpResponse
from django.contrib import admin
from .models import User


admin.site.register(User)



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'price', 'stock', 'is_active')
    list_filter = ('company', 'is_active')
    search_fields = ('name',)
    actions = ['mark_inactive']

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected products as inactive"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'company', 'quantity', 'status', 'shipped_at')
    list_filter = ('company', 'status')
    search_fields = ('product__name',)
    actions = ['export_orders_csv']

    def export_orders_csv(self, request, queryset):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Product', 'Company', 'Quantity', 'Status', 'Shipped At'])

        for order in queryset:
            writer.writerow([
                order.id,
                order.product.name,
                order.company.name,
                order.quantity,
                order.status,
                order.shipped_at or '',
            ])

        return response

    export_orders_csv.short_description = "Export selected orders to CSV"