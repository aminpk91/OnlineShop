from django.contrib import admin
from .models import Productbase,Category,ImageProduct,Cat_attr,Product_attr,Brands
# Register your models here.
# admin.site.register(Product_attr)
# admin.site.register(Cat_attr)
admin.site.register(Brands)

class AttrInline(admin.StackedInline):
    model = Cat_attr
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [AttrInline]


class ImageInline(admin.TabularInline):
    model = ImageProduct
    extra = 1

class AttrsInline(admin.TabularInline):
    model = Product_attr
    extra =1

@admin.register(Productbase)
class ProductAdmin(admin.ModelAdmin):
    inlines = [AttrsInline, ImageInline]
    list_display = ('name','category','brand', 'qty', 'price', 'rate')
    list_filter = [ 'category','brand','rate','name']
