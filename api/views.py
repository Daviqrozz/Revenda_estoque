from django.shortcuts import render,HttpResponse
from .models import Product,Category

def product_view(request):
        
        if request.method == 'GET':
                products = Product.objects.all()
                category = Category.objects.all()
                
                context = {
                        'products_list':products,
                        'categories_list':category
                }
              
                return render(request,'views/products.html',
                              context)

def create_view(request):
    return render(request,'views/create.html')