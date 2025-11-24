
from django.urls import path
from .views import product_view,create_view,edit_view

urlpatterns = [
    path('', product_view, name='products_view'),
    path('create', create_view, name='create_view'),
    path('edit/<int:id>/', edit_view, name='edit_view')
]
