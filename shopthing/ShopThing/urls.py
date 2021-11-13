
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('product.urls')),
    path('', include('users.urls')),
    path('', include('order.urls')),
    path('', include('cart.urls')),
    path('', include('blog.urls')),
    path('', include('payment.urls')),
    path('contact-us', contact,name='contact'),


              ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              # + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
