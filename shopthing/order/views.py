import uuid

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import UserProfile,User,Address
from product.models import Productbase
from order.models import OrderItem,Order
from cart.basket import Basket


def add_orders(request):
    if request.method =='GET':
        #if not request.user.is_anonymous():
        user =User.objects.filter(username=request.user)[0]
        print(user)
        order_id = uuid.uuid1()
        order = Order.objects.create(id=order_id,user=user)
        basket = Basket(request)
        order.amount = basket.get_total_price()
        for item in basket.__iter__():

            OrderItem.objects.create(cart=order,product=item['product'], qty=item['qty'])
            product=Productbase.objects.filter(id=item['product'].id)[0]
            product.qty=product.qty-item['qty']
            product.save()
            basket.delete(product=item['product'])



        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()

        order.save()
        return render(request,'checkout-step-2.html',{'order':order.id,
                                                      'qty': basketqty, 'subtotal': baskettotal})

@csrf_exempt
def shipping(request,order_id):
    order = Order.objects.filter(id=order_id)[0]
    if request.method =='POST':
        if request.POST.get('address'):
            adr_id=request.POST.get('address')
            address = Address.objects.filter(id=adr_id)[0]

        elif request.POST.get('state') and request.POST.get('city') and request.POST.get('new_address'):
            print(request.POST.get('new_address'))
            address = Address.objects.create(userinfo=request.user,state=request.POST.get('state'),city =request.POST.get('city'),address=request.POST.get('new_address'))
        order.shipping_address = address
        ship_method = request.POST.get('ship','delivery')
        order.shipping = ship_method
        order.save()
        return render(request,'checkout-step-3.html',{'order':order})

