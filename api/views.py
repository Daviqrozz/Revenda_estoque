from django.shortcuts import render,get_object_or_404,redirect
from .models import Product,STATUS_OPTIONS,Category,STATUS_SALED,STATUS_IN_STOCK
from .forms import ProductForm,CategoryForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

@login_required
def product_view(request):
    
    products = Product.objects.all()
    
    thirty_days_ago = timezone.now() - timedelta(days=30)

    recent_products = Product.objects.filter(cadastred_date__gte=thirty_days_ago)
    
    new_products_count = recent_products.count()

    sold_recent = recent_products.filter(status=STATUS_SALED)
    
    total_sales = sold_recent.aggregate(total=Sum('sale_value'))['total'] or 0
    total_cost = sold_recent.aggregate(total=Sum('cost'))['total'] or 0

    last_month_balance = total_sales - total_cost

    stock_count = Product.objects.filter(status=STATUS_IN_STOCK).count()

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
        'new_products_count': new_products_count,
        'last_month_balance': last_month_balance,
        'stock_count': stock_count,   
    }
    
    return render(request, 'views/products.html', context)

@login_required
def create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect('products_view')

    form = ProductForm()
    form_category = CategoryForm()
    
    context = {
        'form':form,
        'form_category':form_category
    }
    
    return render(request, 'views/create.html',context)

@login_required
def create_category_view(request):
    if request.method == "POST":
        form_category = CategoryForm(request.POST)
        next_url = request.POST.get('next') 
        
        print("Valor recebido para NEXT:", next_url) 
        
        print("Dados completos do POST:", request.POST) 
        
        if form_category.is_valid():
            form_category.save()
            
            if next_url:

                print(f"Redirecionando com sucesso para: {next_url}")
                return redirect(next_url)
            
            return redirect('products_view')
            
    return redirect('products_view')
@login_required
def edit_view(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        
        if form.is_valid():

            form.save()
            return redirect('products_view')

    else:
        form = ProductForm(instance=product)
        form_category = CategoryForm()
        
    context = {
        'form': form,
        'product': product,
        'form_category':form_category
    }
    
    return render(request, 'views/edit.html', context)
@login_required
def delete_view(request, id):
    product = get_object_or_404(Product,pk=id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products_view')
    
    return redirect('products_view')
    
    
        