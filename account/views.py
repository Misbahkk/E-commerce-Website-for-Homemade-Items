from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Profile ,userProfile
from .forms import UserProfileForm

from siteApp.models import *
from account.models import Cart, CartItems

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.urls import reverse




# Create your views here.

def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email).first()
        if not user_obj:
            messages.warning(request, "Account Not found")
            return HttpResponseRedirect(request.path_info)
        
        if not user_obj.profile.is_email_varified:
            messages.warning(request,'Ypu acount is not verified')
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email , password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('/')

       
        messages.warning(request,'Invalid creditional')
        return HttpResponseRedirect(request.path_info)
    return render(request, 'accounts/login.html')

def logout_user(request):
    
    logout(request)
    return redirect('/')


def register_page(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = email)
        if user_obj:
            messages.warning(request, "Email alredy exit")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name=first_name,last_name=last_name,username= email,email=email)
        user_obj.set_password(password)
        user_obj.save()
        messages.success(request,'An email has been send on you email')
        return HttpResponseRedirect(request.path_info)


        
    return render(request , 'accounts/register.html')




def active_email(request,email_token):
    try:
        user = Profile.objects.get(email_token=email_token)
        user.is_email_varified=True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid link')
    




@login_required
def add_to_cart(request,uid):
    try:
        products = Product.objects.get(uid=uid)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user,is_paid=False)

        cart_item = CartItems.objects.filter(cart=cart,product=products).first()
        if cart_item:
            messages.error(request, "Product Alredy present in cart")
        else:

            cart_item, created = CartItems.objects.get_or_create(cart = cart , product= products)
            messages.success(request, "Item added to cart successfully!")
            if not created:
                cart_item.quantity += 1
                cart_item.save()
    except Product.DoesNotExist:
        messages.error(request, "Product does not exist.")
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong. Please try again.")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_cart(request,cart_item_uid):
    try:
        carta_item = CartItems.objects.get(uid = cart_item_uid)
        carta_item.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart(request):

    cart_obj = Cart.objects.filter(is_paid=False, user=request.user).first()  
    if request.method == 'POST':
        if not cart_obj:
            messages.warning(request, "You don't have an active cart.")
            return redirect('cart')  
        coupon = request.POST.get('coupon')
        coupon_obj = Coupon.objects.filter(coupn_code__icontains = coupon)
        if not coupon_obj.exists():
           
            messages.warning(request, "Account Not found")
            print("Invalid coupon code : -> ")
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(request.path_info)
        
        if cart_obj.coupon:
            messages.warning(request,"Coupon alredy exit..")
            print("Coupon alredy exit..")
            # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            return HttpResponseRedirect(request.path_info)
        

        if cart_obj.get_cart_total() < coupon_obj[0].minimum_amount:
            messages.warning(request, f"Amount Sould be greater that {coupon_obj[0].minimum_amount}")
            print(f"Amount Sould be greater that {coupon_obj[0].minimum_amount}")
            return HttpResponseRedirect(request.path_info)
        
        if coupon_obj[0].is_expire:
            messages.warning(request, "Coupon Expired")
            print("Coupon Expired")
            return HttpResponseRedirect(request.path_info)



        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request,"Coupon Applied..")
        print("Coupon Applied..")
        print("POST data:", request.POST)
        print("Coupon code:", coupon)
        print("Coupon exists:", coupon_obj.exists())
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # repturn HttpResponseRedirect(request.path_info)

    context = {'cart':cart_obj}
    
    return render(request, 'accounts/cart.html', context)



from datetime import datetime, timedelta
import hmac
import hashlib


JAZZCASH_MERCHANT_ID = "MC143920"
JAZZCASH_PASSWORD = "73sb91dshv"
JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/account/success/"
JAZZCASH_INTEGRITY_SALT = "xz1y1ashz1"

@login_required
def checkout(request):
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
        
    except Cart.DoesNotExist:
        # Handle the case where the cart doesn't exist
        messages.error(request, "You don't have any items in your cart to checkout.")
        return redirect('cart')  # Redirect to the cart page

    # # Calculate total amount
    total_amount = cart_obj.get_cart_total()
    total_amount_paisa = int(total_amount )  # Convert to paisa



    current_datetime = datetime.now()
    pp_TxnDateTime = current_datetime.strftime('%Y%m%d%H%M%S')

    expiry_datetime = current_datetime + timedelta(hours=1)
    pp_TxnExpiryDateTime = expiry_datetime.strftime('%Y%m%d%H%M%S')

    pp_TxnRefNo = "T" + pp_TxnDateTime
    post_data = {
        "pp_Version": "1.0",
        "pp_TxnType": "",
        "pp_Language": "EN",
        "pp_MerchantID": JAZZCASH_MERCHANT_ID,
        "pp_SubMerchantID": "",
        "pp_Password": JAZZCASH_PASSWORD,
        "pp_BankID": "TBANK",
        "pp_ProductID": "RETL",
        "pp_TxnRefNo": pp_TxnRefNo,
        "pp_Amount": total_amount_paisa,
        "pp_TxnCurrency": "PKR",
        "pp_TxnDateTime": pp_TxnDateTime,
        "pp_BillReference": "billRef",
        "pp_Description": "Description of transaction",
        "pp_TxnExpiryDateTime": pp_TxnExpiryDateTime,
        "pp_ReturnURL": JAZZCASH_RETURN_URL,
        "pp_SecureHash": "",
        "ppmpf_1": "1",
        "ppmpf_2": "2",
        "ppmpf_3": "3",
        "ppmpf_4": "4",
        "ppmpf_5": "5"
    }

    sorted_string = "&".join(f"{key}={value}" for key , value in sorted(post_data.items()) if value != "")
    pp_SecureHash = hmac.new(
        JAZZCASH_INTEGRITY_SALT.encode(),
        sorted_string.encode(),
        hashlib.sha256
    ).hexdigest()
    post_data['pp_SecureHash'] = pp_SecureHash

    context = {
        'cart':cart_obj,
        "product_price" : total_amount,
        'post_data':post_data
    }
    print(f"'cart':{cart_obj},'product_price' :{ total_amount},'post_data':{post_data}")
    return render(request, 'accounts/checkout.html', context)





@csrf_exempt
@login_required
def payment_success(request):
    print("adding 000")
    received_data = request.POST.dict()
    print("Received data: ", received_data)

    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to login page if user is anonymous
        return HttpResponseRedirect(reverse('login'))

    # Fetch the user's unpaid cart
    cart = Cart.objects.filter(is_paid=False, user=request.user).first()
    print("cart: ", cart)

    if cart:
        cart.is_paid = True
        cart.payment_id = received_data.get('pp_TxnRefNo')  # Transaction reference
        cart.payment_method = "JazzCash"
        cart.payment_date = datetime.now()
        cart.save()

    return render(request, 'accounts/success.html')




def remove_coupon(request,cart_id):
    cart = Cart.objects.get(uid = cart_id)
    cart.coupon = None
    cart.save()
    messages.warning(request, "Coupon Successfully removed")
    print("Coupon Successfully removed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def dashboard(request):
    paid_carts = Cart.objects.filter(is_paid=True, user=request.user).order_by('-payment_date')
    user_profile , created = userProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=user_profile)
        if  form.is_valid():
            form.save()
            return redirect('my_account')
    
    else:
        form = UserProfileForm(instance=user_profile)



    context = {
        'paid_carts': paid_carts,
        'form':form,
    }
    return render(request,'accounts/my_account.html',context)


def contactUs(request):
    return render(request, 'accounts/contact.html')