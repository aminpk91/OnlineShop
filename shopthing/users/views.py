import threading

from django.contrib.auth.models import User
from django.shortcuts import render,get_object_or_404
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login as log_in, logout as log_out
from django.db import IntegrityError
from .tasks import phone_verification,say_hello

from order.models import Order

# from utils.phone_verification import phone_verification
from django.core.cache import cache

#from .models import SupplierProfile

#phone_cache = caches['phone_verification']


# Create your views here.
from users.models import UserProfile,User


# from utils.phone_verification import phone_verification


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", None)
        #print(username)
        if username:
            password = request.POST.get('password', None)
            #print(password)
            if password:
                if UserProfile.objects.filter(user__username=username).exists():
                    user = UserProfile.objects.filter(user__username=username)[0]
                    if user.verified:
                        user = authenticate(request, username=username, password=password)
                        if user:
                            log_in(request, user)
                            messages.success(request, 'شما با موفقیت وارد شدید!')
                            return redirect("/")
                        else:
                            messages.error(request, 'نام کاربری یا رمز اشتباه')
                            return redirect("/")
                    else:
                        user = User.objects.filter(username__iexact=username)[0]
                        context = {'user': user.id}
                        return render(request,'regenrate_code_vrification.html',context)
        else:
            messages.warning(request, 'نام کاربری الزامی ست')
            return redirect("/")


def logout_view(request):
    log_out(request)
    return redirect('/')

def signup(request):
    say_hello.delay()
    if request.method == "POST":
        username = request.POST.get("username", None)

        phone = request.POST.get("phone", None)
        first_name = request.POST.get("firstname", None)
        last_name = request.POST.get("lastname", None)
        if username:
            if User.objects.filter(username__iexact=username).count() == 0:
                password = request.POST.get('password', None)
                repeated_passweord = request.POST.get('repassword', None)
                if password:
                    if password == repeated_passweord:
                        try:
                            user = User.objects.create_user(username=username,email=None, password=password, first_name=first_name,last_name=last_name,is_active=False)
                            profile = get_object_or_404(UserProfile,user=user)
                            profile.phone = phone
                            profile.save()
                            print(user.id, profile.phone)
                            phone_verification.delay(user.id, profile.phone)
                            return render(request, 'phone_verification.html',context={'user': user.id})
                        except IntegrityError as e:
                            # return render(request, "user/error.html", {"message": e})
                            messages.error(request, f"{e}")
                            return redirect('/')

                    else:
                        messages.error(request, "عدم انطباق پسوورد")
                        return redirect('/')
            else:
                user = User.objects.filter(username__iexact=username)[0]
                print(user.id)
                context = {'user': user.id}
                return render(request, 'regenrate_code_vrification.html', context)


def dashboard(request):
    user = request.user
    #user = UserProfile.objects.filter(user=user)
    orders = Order.objects.filter(user=user)
    return render(request, 'dashboard.html', {'orders' : orders})


def phone_register(request,user):
    if request.method == 'POST':
        code = request.POST.get("code",None)
        user = User.objects.get(id=user)
        print(code)
        print(cache.get(f"code:{user.id}"))
        if code:
            if int(cache.get(f"code:{user.id}")) == int(code):
                user.is_active = True
                user.save()
                profile = get_object_or_404(UserProfile,user_id=user.id)
                profile.verified = True
                profile.save()
                #Cart.objects.create(user=profile)
                user = authenticate(request, username=user.username, password=user.password)
                if user:
                    log_in(request, user)
                    messages.success(request, 'شما با موفقیت وارد شدید!')
                    return redirect("/")
                else:
                    return redirect("/")

            else:
                return HttpResponse("code invalid or expired")
        else:
            return HttpResponse("no code")

    if request.method == 'GET':
        return render(request, 'phone_verification.html',context={'user':user})



def phone_register_again(request,user):

    if request.method == 'GET':
        puser = UserProfile.objects.filter(user_id=user)[0]
        if puser.phone:
            print(puser.phone)
            thread = threading.Thread(target=phone_verification, args=(puser.user.id, puser.phone))
            thread.start()

            return redirect(f'/phone_register/{user}')
        #return render(request, 'phone_verification.html',context={'user':puser.id})
        else:
            return HttpResponse('dont have phone')