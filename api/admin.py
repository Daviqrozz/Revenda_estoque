from django.contrib import admin
from .models import Category,Product
from django.contrib.auth.models import User, Group

admin.site.unregister(User)
admin.site.unregister(Group)

admin.site.register(Category) 
# 2. Registro com Personalização (para o Produto)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # O Admin usará estas configurações:
    list_display = ('name', 'quantity_total', 'quantity_sold', 'quantity_in_stock', 'sale_value', 'total_profit')
    list_filter = ('category', 'sale_value')
    search_fields = ('name', 'observation')