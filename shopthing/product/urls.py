
from django.contrib import admin
from django.urls import path
from .views import index,ProductList,ProductDetail,add_comment

urlpatterns = [
    path('', index,name='index'),
    path('product-list/', ProductList.as_view(),name='product-list'),
    path('product-detail/<str:slug>/', ProductDetail.as_view(), name='product-detail'),
    path('product/add-comment/<int:aid>/', add_comment, name='product-add-comment'),

]
