from django.urls import path
from .views import login_view,logout_view,signup,dashboard,phone_register,phone_register_again




urlpatterns = [
    path('register/', signup, name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('dashboard/',dashboard,name='dashboard'),
    #path('activate/<str:uidb64>/<str:token>', email_activate, name='activate'),
    path('phone_register/<int:user>',phone_register,name='phone_register'),
    path('phone_register_again/<int:user>',phone_register_again,name='phone_register_again'),
   # path('supplier_register/',supplier_register,name='supplier_register'),
   # path('email_reactive/<int:user>',re_gen_email_activate,name='email_reactive'),


]