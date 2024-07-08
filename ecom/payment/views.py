from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import *
from payment.models import *
from django.shortcuts import  get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User

def billing_info(request):
    if request.POST:
        #GET the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        #create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

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

def process_order(request):
    if request.POST:
        # GET the cart
        cart = Cart(request)
        cart_products = cart.get_prods
        totals = cart.cart_total()

        # Debugging print statement
        print(f"Cart total: {totals}")

        # GET Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping Session Data
        my_shipping = request.session.get('my_shipping')

        if not my_shipping:
            messages.error(request, "Shipping information is missing.")
            return redirect('checkout')  # Redirect to the appropriate page

        # Gather order info 
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        # Create shipping address from session info
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}\n"
            f"{my_shipping['shipping_state']}\n"
            f"{my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}"
        )

        amount_paid = totals

        if amount_paid is None:
            messages.error(request, "Amount paid calculation failed.")
            return redirect('checkout')  # Redirect to the appropriate page

        if request.user.is_authenticated:
            # Logged in
            user = request.user
        else:
            # Not logged in
            user = None  # or handle anonymous user appropriately

        # Create order
        create_order = Order(
            user=user,
            full_name=full_name,
            email=email,
            shipping_address=shipping_address,
            amount_paid=amount_paid
        )
        create_order.save()
        messages.success(request, "Order placed!")
        return redirect('home')

    else:
        messages.error(request, "Access denied")
        return redirect('home')