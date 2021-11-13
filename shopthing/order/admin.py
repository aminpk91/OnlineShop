from django.contrib import admin
from .models import  OrderItem,Order
# Register your models here.
admin.site.register(OrderItem)
#
class ItemInline(admin.StackedInline):
    model = OrderItem
    extra = 3


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ItemInline]