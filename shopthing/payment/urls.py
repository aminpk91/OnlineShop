from django.urls import path , include
from . import views

urlpatterns = [

    path('payment/', views.home, name='home'),
    path('gateway/<str:order>/', views.gateway, name='gateway'),
    path('payment/return/', views.payment_return, name='payment_return'),
    path('payment/check/<pk>', views.payment_check, name='payment_check'),
    # path('requirement', views.requirement, name='requirement'),
    # path('about-me', views.about_me, name='about_me'),
]