from django.contrib import admin
from .models import OrderItem, Product, Order, Message, Vendor

admin.site.site_header = 'Stock Dashboard'

#create display table in admin dashboard

class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')
    list_filter = ['category',]
# Register your models here.

admin.site.register(Product, ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Message)
admin.site.register(Vendor)
