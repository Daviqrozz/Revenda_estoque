from django.shortcuts import render
# Importe a constante STATUS_OPTIONS do seu models.py
from .models import Product, Category, STATUS_OPTIONS 


def product_view(request):
    
   
    products = Product.objects.all()
 
    

    selected_status = request.GET.get('status')
    
    status_filter_value = None
    

    if selected_status and selected_status.isdigit():
 
        status_filter_value = int(selected_status)
        
    if status_filter_value is not None:

        products = products.filter(status=status_filter_value)
            

    context = {
        'products_list': products,
        'selected_status': selected_status, 
        'status_choices': STATUS_OPTIONS,    
    
    }
    
    return render(request, 'views/products.html', context)


def create_view(request):
    return render(request, 'views/create.html')