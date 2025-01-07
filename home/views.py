from django.shortcuts import render, get_object_or_404
from siteApp.models import Product ,Category



# Create your views here.

def index(request):
    categories = Category.objects.all()  
    products =Product.objects.all()

    name_filter = request.GET.get("name")
    price_range_filter = request.GET.get('price_range','')

    if name_filter:
        products = products.filter(title__icontains=name_filter)
    
    if price_range_filter:
        price_max,price_min = map(int,price_range_filter.split('-'))
        products = products.filter(price__gte = price_min,price__lte=price_max)
    


    context ={'products':products , 'categories':categories}
    return render(request,'home/index.html',context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()  # Related products through the ForeignKey
    return render(request, 'category_detail.html', {'category': category, 'products': products})