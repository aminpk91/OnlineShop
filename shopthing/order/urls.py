
from django.contrib import admin
from django.urls import path
from .views import add_orders,shipping

urlpatterns = [
    path('order/', add_orders, name='order'),
    path('shipping/<str:order_id>', shipping, name='shipping'),

    # path('order/gateway', gateway, name='gateway'),

]