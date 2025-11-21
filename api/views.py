from django.shortcuts import render

def product_view(request):
    return render(request,'views/products.html',)

def create_view(request):
    return render(request,'views/create.html')