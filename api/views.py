from django.shortcuts import render,get_object_or_404,redirect
from .models import Product, Category, Sale
from .forms import ProductForm, CategoryForm, SaleForm
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

    # Calculate balance from Sale records in the last 30 days
    recent_sales = Sale.objects.filter(created_at__gte=thirty_days_ago)
    
    total_sales = recent_sales.aggregate(total=Sum('price_sold'))['total'] or 0
    
    # Calculate total cost for sold items (cost per unit * quantity sold)
    total_cost = 0
    for sale in recent_sales:
        total_cost += sale.product.cost * sale.quantity
    
    last_month_balance = total_sales - total_cost

    # Count products with stock available
    stock_count = sum(1 for p in Product.objects.all() if p.quantity_in_stock > 0)

    # Optional: Filter by stock status
    stock_filter = request.GET.get('stock')
    
    if stock_filter == 'in_stock':
        products = [p for p in products if p.quantity_in_stock > 0]
    elif stock_filter == 'sold_out':
        products = [p for p in products if p.quantity_in_stock <= 0]

    # Pagination
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10) # 10 products per page

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products_list': products,
        'stock_filter': stock_filter,
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

@login_required
def sell_product_view(request, id):
    product = get_object_or_404(Product, pk=id)
    
    if request.method == 'POST':
        form = SaleForm(request.POST)
        
        if form.is_valid():
            sale = form.save(commit=False)
            
            # Double-check stock availability
            if sale.quantity > product.quantity_in_stock:
                form.add_error('quantity', f'Quantidade indisponível. Estoque atual: {product.quantity_in_stock}')
            else:
                sale.save()
                return redirect('products_view')
    else:
        # Pre-fill the form with the selected product
        form = SaleForm(initial={
            'product': product,
            'price_sold': product.sale_value,
            'quantity': 1
        })
    
    context = {
        'form': form,
        'product': product,
    }
    
    return render(request, 'views/sell.html', context)
    
    