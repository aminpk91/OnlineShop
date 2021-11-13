import uuid
from django.db import models
from users.models import UserProfile,User,Address
from product.models import Productbase
# Create your models here.



class Order(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    choices = (
        ('paid', 'پرداخت شده'),
        ('approve_needed', 'در انتظار تایید'),
        ('pending', 'در انتظار پرداخت'),
        ('failed', 'ناموفق'),
    )
    ship_choices = (
        ('delivery', 'پیک'),
        ('tipax', 'تیپاکس'),
        ('porterage', 'باربری'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64, choices=choices, default='pending')
    amount = models.DecimalField(default=0, max_digits=13, decimal_places=2)
    shipping = models.CharField(max_length=10,choices=ship_choices,default='delivery',null=True)
    shipping_address = models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)

    # class Meta:
    #     unique_together = (("user", "created_at"),)

class OrderItem(models.Model):

    cart = models.ForeignKey(to=Order, on_delete=models.CASCADE ,related_name='cart')
    product = models.ForeignKey(to=Productbase, on_delete=models.CASCADE, related_name='product_in_cart')
    qty = models.IntegerField(default=1)
    description = models.TextField(default="پیام فروشگاه ایرانیان برای شما")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args,**kwargs):
        if self.qty > self.product.qty:
            diff = self.qty-self.product.qty
            self.qty = self.product.qty
            self.description = f'{diff} عدد بیش از موجودی سفارش داده شده است. '

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.product.name} , {self.cart.user}'