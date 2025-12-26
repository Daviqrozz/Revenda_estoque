# forms.py

from django import forms
from .models import Product, Category, Sale

# Defina a string de classes comuns para facilitar a manutenção
INPUT_CLASSES = 'form-control bg-card text-primary'
SELECT_CLASSES = 'form-select bg-card flex-grow-1'

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = [
            'name',
            'observation',
            'category',
            'quantity_total',
            'cost',
            'sale_value'
        ]
        
        widgets = {
            # 1. Campo 'name': TextInput para inputs simples
            'name': forms.TextInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Nome do Produto'
                }
            ),

            # 2. Campo 'category': Select para ForeignKeys
            'category': forms.Select(
                attrs={
                    'class': SELECT_CLASSES,
                    # Adicione o atributo required se necessário (embora o Django Model já faça isso)
                    'required': True 
                }
            ),
            
            # 3. Campo 'quantity_total': NumberInput para Inteiros
            'quantity_total': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Ex: 10 unidades',
                    'min': 0 # Adiciona a restrição min="0" diretamente
                }
            ),
            
            # 4. Campos de Valor (Cost e Sale_value): NumberInput para Decimais
            'cost': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Ex: R$ 50,00 (por unidade)',
                    'min': 0,
                    'step': '0.01' # Para permitir valores decimais
                }
            ),
            'sale_value': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Ex: R$ 80,00 (por unidade) - Opcional',
                    'min': 0,
                    'step': '0.01'
                }
            ),
            
            # 5. Campo 'observation': Textarea para textos longos
            'observation': forms.Textarea(
                attrs={
                    'class':INPUT_CLASSES,
                    'placeholder':'Observações',
                    'rows':3
                }
            ),
        }
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'name'
        ]
        widgets = {
            'name':forms.TextInput(
                attrs={
                    'class':INPUT_CLASSES,
                    'placeholder':'Digite o nome da categoria'
                }
            )
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['product', 'quantity', 'price_sold']
        
        widgets = {
            'product': forms.Select(
                attrs={
                    'class': SELECT_CLASSES,
                    'required': True
                }
            ),
            'quantity': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Quantidade a Vender',
                    'min': 1
                }
            ),
            'price_sold': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Valor de Venda (R$)',
                    'min': 0,
                    'step': '0.01'
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter products to only show those with stock
        from .models import Product
        self.fields['product'].queryset = Product.objects.filter(quantity_total__gt=0)
    
    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')
        
        if product and quantity:
            if quantity > product.quantity_in_stock:
                raise forms.ValidationError(
                    f'Quantidade indisponível. Estoque atual: {product.quantity_in_stock} unidades.'
                )
        
        return cleaned_data