from django.shortcuts import render ,redirect
from account.models import Cart, CartItems,Profile
from siteApp.models import Product
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
def get_product(request,slug):    
    try:
        products = Product.objects.get(slug=slug)

        return render(request,'product/product.html',context={'products':products})
    except Product.DoesNotExist:
        raise Http404("Product not found")
    except Exception as e:
        print(e)


