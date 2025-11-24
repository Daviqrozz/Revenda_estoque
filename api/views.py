from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,STATUS_OPTIONS
from .forms import ProductForm

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

def edit_view(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():

            form.save()
            return redirect('products_view')

    else:
        form = ProductForm(instance=product)
        
    context = {
        'form': form,
        'product': product
    }
    
    return render(request, 'views/edit.html', context)