from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
from django.db.models import Q
import json
from cart.cart import Cart

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html',{'products':products})

def about(request):
    return render(request, 'about.html',{})

def login_user(request):
    if request.method == "POST":
        username =  request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request, user)
            #do some shopping cart stuff
            current_user = Profile.objects.get(user__id = request.user.id)
            #GET their saved cart from datebase
            saved_cart = current_user.old_cart
            #Convert database string to python dictionary
            if saved_cart:
                #convert to dictionary using JSON
                converted_cart = json.loads(saved_cart)
                #Add the loaded cart dictionary to our session
                #get the cart
                cart = Cart(request)
                #Loop throw the cart and add the items from the database 
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value)
            
            messages.success(request,("YOU have been loged in!"))
            return redirect('home')
        else:
            messages.success(request,("there was an error !please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,("you have been log out"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request,("Username Created - please Fill out user Info Below..."))
            return redirect('update_info')
        else:
            messages.success(request,("whops have problem please try again!!"))
            return redirect('register')
    else:
        return render(request, 'register.html',{'form':form})
def product(request,pk):
    product = Product.objects.get(id = pk)
    return render(request, 'product.html',{'product':product})
def category(request, foo):
    #Replace Hyphens with spaces
    foo = foo.replace('-',' ')
    #Grab the category from the url
    try:
        #look up the category
        category = Category.objects.get(name = foo)
        products = Product.objects.filter(category = category)
        return render(request,'category.html',{'products':products,'category':category})

    except:
        messages.success(request,("that category doesn't exist"))
        return redirect ('home')
def ticket(request):
    if request.method == "POST":
        ticket_obj = Ticket.objects.create()
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
    else:
        form = TicketForm()
    return render(request, 'tickect.html',{'form':form})


def category_summary(request):
    categories = Category.objects.all
    return render(request,'category_summary.html',{"categories":categories})
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance = current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            messages.success(request,"User Has been updated!!")
            return redirect('home')
        return render(request,"update_user.html",{'user_form':user_form})


    else:
        messages.success(request,"you must BE logged In to access to pages")
        return redirect('home')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out rhe form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user,request.POST)
            #IS the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been updated , please logged in again....")
                #login(request,current_user)
                return redirect('login')
            else:
                for error in List(form.errors.values()):
                    messages.error(request,error)
        else:
            form = ChangePasswordForm(current_user)
            return render(request,"update_password.html",{'form':form})
    else:
        messages.success(request,"YOU MUST BE LOGGED IN TO VIEW THAT PAGE..")
        return redirect('home')


def update_info(request):
        if request.user.is_authenticated:
            #Get current User
            current_user = Profile.objects.get(user__id = request.user.id)
            #Get Current User's shipping info
            shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
            #Get original User Form
            form = UserInfoForm(request.POST or None,instance = current_user)
            
            #Get User's shipping Form
            shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
            if form.is_valid() or shipping_form.is_valid():
                #save original form
                form.save()
                #save shipping form
                shipping_form.save()

                messages.success(request,"your info has been updated!!")
                return redirect('home')
            return render(request,"update_info.html",{'form':form,'shipping_form':shipping_form})


        else:
            messages.success(request,"you must BE logged In to access to pages")
            return redirect('home')
def search(request):
    #determine if they filled out the form
    if request.method == "POST":
        searched = request.POST['searched']
        #Query The Products DB Model 
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        # Test for null
        if not searched:
             messages.success(request,"the product dosen't Exists...please try again")
             return render(request,"search.html",{})
        else:
            return render(request,"search.html",{'searched':searched})
    else:
        return render(request,"search.html",{})