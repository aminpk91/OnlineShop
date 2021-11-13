from decimal import Decimal
from datetime import datetime

import pytz
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from order.models import Order
from .models import Invoice
from django.views.decorators.csrf import csrf_exempt
from decouple import config
from idpay.api import IDPayAPI

import requests
import json
import uuid


def payment_init():
    base_url = config('BASE_URL', default='http://127.0.0.1:8044/', cast=str)
    api_key = config('IDPAY_API_KEY', default='2636170d-96e5-471e-b477-44fcdb4592a3', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)


def home(request):
    payments = Invoice.objects.all()
    return render(request, 'home.html', {'payments': payments})


def gateway(request, order):
    if request.method == 'GET':
        print(order)
        order_id = order
        order = Order.objects.filter(id=order_id)[0]
        print(order)

        amount = float(order.amount)

        payer = {
            'name': f'{request.user.first_name} {request.user.last_name}'

        }

        record = Invoice(order_id=str(order_id), amount=int(amount))
        record.save()

        idpay_payment = payment_init()
        result = idpay_payment.payment(str(order_id), amount, 'payment/return/', payer)

        if 'id' in result:
            record.status = 1
            record.payment_id = result['id']
            record.save()

            return redirect(result['link'])

        else:
            txt = result['message']
    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


@csrf_exempt
def payment_return(request):
    if request.method == 'POST':

        pid = request.POST.get('id')
        status = request.POST.get('status')
        pidtrack = request.POST.get('track_id')
        order_id = request.POST.get('order_id')
        amount = request.POST.get('amount')
        card = request.POST.get('card_no')
        date = request.POST.get('date')
        print(order_id, type(str(order_id)))
        order = Order.objects.filter(id=order_id)
        if Invoice.objects.filter(order_id=order_id, payment_id=pid, amount=amount, status=1).count() == 1:

            idpay_payment = payment_init()
            print(date)
            payment = Invoice.objects.get(payment_id=pid, amount=amount)
            payment.status = status
            payment.date = datetime.fromtimestamp(int(date)).replace(tzinfo=pytz.UTC)
            payment.card_number = card
            payment.idpay_track_id = pidtrack
            payment.save()

            if str(status) == '10':
                result = idpay_payment.verify(pid, payment.order_id)

                if 'status' in result:

                    payment.status = result['status']
                    payment.bank_track_id = result['payment']['track_id']
                    payment.save()
                    if result['status'] == 100:
                        order.update(status='paid')
                    return render(request, 'bill.html', {'txt': result['message'],
                                                         'payment': payment,

                                                         })

                else:
                    txt = result['message']

            else:
                txt = "Error Code : " + str(status) + "   |   " + "Description : " + idpay_payment.get_status(status)

        else:
            txt = "Order Not Found"

    else:
        txt = "Bad Request"

    return render(request, 'error.html', {'txt': txt})


def payment_check(request, pk):
    payment = Invoice.objects.get(pk=pk)
    # order = Order.objects.filter(id=payment.order_id)
    # print(order)
    idpay_payment = payment_init()
    result = idpay_payment.inquiry(payment.payment_id, payment.order_id)

    if 'status' in result:
        payment.status = result['status']
        payment.idpay_track_id = result['track_id']
        payment.bank_track_id = result['payment']['track_id']
        payment.card_number = result['payment']['card_no']
        payment.date = str(result['date'])
        payment.save()
        # if result['status'] == 100:
        #     order.update(status='paid')

    return render(request, 'error.html', {'txt': result['message']})

