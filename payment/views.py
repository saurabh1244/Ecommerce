from django.shortcuts import render , HttpResponse , redirect
from . models import Product , Category , Profile
from django.contrib.auth import login ,logout , authenticate
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm  , UpdateUserForm , ChangePasswordForm , UserInfoForm
from django import forms
from django.db.models.signals import post_save
from django.db.models import Q
import json
from cart.cart import Cart


from payment.forms import ShippingForm
from payment.models import ShippingAddress


def home(request):
    obj = Product.objects.all()
    return render(request,'index.html' ,{"product": obj})


def about(request):
    return render(request,'about.html')




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username, password=password)
        if user is not None:
            login(request,user)

            current_user = request.user

            # obj  = Profile.objects.get(user = current_user)
            current_user  = Profile.objects.get(user__id = request.user.id)
            saved_cart = current_user.old_cart

            if saved_cart:
                converted_cart = json.loads(saved_cart)
                cart = Cart(request)

                for key, value in converted_cart.items():
                    cart.db_add(product=key, quantity=value)
               
            



            messages.success(request ,('You haved been Logged in successfully'))
            return redirect('home')
        else:
            messages.success(request ,('Got an Error! Please try again'))
            return redirect('login')
        
    else:
        return render(request,'login.html')
    



def register_user(request):
    form  = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request ,('You haved been Logged in successfully'))
            return redirect('update_info')
        
        else:
            messages.success(request ,('Something got error'))
            return redirect('register')


    else:
        return render(request,'register.html',{'form':form})



def logout_user(request):
    logout(request)
    messages.success(request , 'you sucessfully logged out')
    return redirect('home')



def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html',{'products':product})



def category(request,foo):
    category = Category.objects.get(name=foo)
    product = Product.objects.filter(category=category)
    return render(request, 'category.html',{'product':product,'category':category})


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html',{"categories":categories})



def update_user(request):
    if request.user.is_authenticated:
        current_users = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_users)

        if user_form.is_valid():
            user_form.save()

            login(request, current_users)
            messages.success(request, (" user has been updated...."))
            return redirect('home')
       
        return render(request , "update_user.html",{"user_form":user_form})
    else:
         messages.success(request, (" you must logged in ...."))
         return redirect('home')
    


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user

        if request.method == 'POST':
            form = ChangePasswordForm(current_user , request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, (" you password must be updated in...."))
                login(request,current_user)
                return redirect('update_user')
            
            else:
                for error in list(form.errors.values()):
                    messages.error(request , error)
                    return redirect('update_password')


        else:
            form = ChangePasswordForm(current_user)
            return render(request , "update_password.html", {"form":form})
        
    else:
        messages.success(request, (" you must be loggde in...."))





def update_info(request):
    if request.user.is_authenticated:
        current_users = Profile.objects.get(user__id=request.user.id)
        form = UserInfoForm(request.POST or None, instance=current_users)
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() or shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, (" Your info  has been updated...."))
            return redirect('home')
       
        return render(request , "update_info.html",{"form":form, "shipping_form":shipping_form})
    else:
         messages.success(request, (" you must logged in ...."))
         return redirect('home')
    




def search(request):
    if request.method == "POST":
        search = request.POST['searched']
        print(f"i got {search}")
        search = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search)  )

        if not search:
            messages.success(request, ('Yur Product not in List..'))
            return redirect('search')
        
        else:
             return render(request , "search.html" ,{'search':search})
    
    else:
        return render(request , "search.html",{})
        
    

    


# def update_info(request):
#     if request.user.is_authenticated:
#         try:
#             current_user = request.user
#             current_profile = Profile.objects.get(user=current_user)  # Use user object for lookup
#             form = UserInfoForm(request.POST or None, instance=current_profile)

#             if form.is_valid():
#                 form.save()
#                 messages.success(request, ("Your info has been updated...."))
#                 return redirect('home')

#             return render(request, "update_info.html", {"form": form})
#         except Profile.DoesNotExist:
#             messages.error(request, ("No profile found for this user. Please create a profile."))
#             return redirect('create_profile')  # Redirect to profile creation view if needed
#     else:
#         messages.success(request, ("You must be logged in ...."))
#         return redirect('home')