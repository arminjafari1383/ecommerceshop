from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import *
from payment.models import ShippingAddress
from django.shortcuts import  get_object_or_404
from django.contrib import messages


def billing_info(request):
    if request.POST:
        #GET the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "billing_info.html",{"cart_products":cart_products,"ShippingForm":ShippingForm,"billing_form":billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, "billing_info.html",{"cart_products":cart_products,"ShippingForm":ShippingForm,"billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "billing_info.html",{"cart_products":cart_products,"shipping_form":shipping_form})

    else:
        messages.success(request,"acesse denid")
        return redirect('home')

def checkout(request):
    #GET the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    if request.user.is_authenticated:
        #checkout as logged in user
        #shipping user
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        #shipping form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "checkout.html",{"cart_products":cart_products,"shipping_form":shipping_form})
    else:
        # checkout as guset
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "checkout.html",{"cart_products":cart_products,"shipping_form":shipping_form})


def payment_success(request):
    
    return render(request, "payment/payment_success.html",{})
