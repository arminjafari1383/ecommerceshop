from django.shortcuts import render,get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
def cart_summary(request):
    #GET the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    totals = cart.cart_total()
    return render(request, "cart_summary.html",{"cart_products":cart_products,"totals":totals})

def cart_add(request):
    #GET the cart
    cart = Cart(request)
    #test for post 
    if request.POST.get('action') == 'post':
        #GET stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))
        #lookup product in db
        product = get_object_or_404(Product,id = product_id)
        #save to session
        cart.add(product = product , quantity = product_qty)
        #get cart  quantity
        cart_quantity = cart.__len__()
        #return response
        # response = JsonResponse({'Product Name: ' :product.name})
        response = JsonResponse({'qty ' :cart_quantity})
        return response
def cart_delete(request):
    #GET the cart
    cart = Cart(request)
    #test for post 
    if request.POST.get('action') == 'post':
        #GET stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))
        #lookup product in db
        product = get_object_or_404(Product,id = product_id)
        #save to session
        cart.delete(product = product)
        #get cart  quantity
        cart_quantity = cart.__len__()
        #return response
        # response = JsonResponse({'Product Name: ' :product.name})
        response = JsonResponse({'qty ' :cart_quantity})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        #GET stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = str(request.POST.get('product_qty'))
        cart.update(product = product_id, quantity = product_qty)
        response = JsonResponse({'qty':product_qty})
        return response
        # return redirect('cart_summary')