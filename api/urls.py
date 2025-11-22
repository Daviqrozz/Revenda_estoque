
from django.urls import path
from .views import product_view,create_view

urlpatterns = [
    path('', product_view, name='products_view'),
    path('/create', create_view, name='create_view')
]
