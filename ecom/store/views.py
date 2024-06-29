from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django import forms

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
            messages.success(request,("your register succesfully"))
            return redirect('home')
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
        current_users = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None,instance = current_user)
