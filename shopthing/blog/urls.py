
from django.contrib import admin
from django.urls import path
from .views import BlogList,BlogDetail,add_comment

urlpatterns = [
    path('blog/', BlogList.as_view(), name='blog'),
    path('blog-detail/<str:slug>/', BlogDetail.as_view(), name='blog-detail'),
    path('blog/add-comment/<int:aid>/', add_comment, name='add-comment'),

]