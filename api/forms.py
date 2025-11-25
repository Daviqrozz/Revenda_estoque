# forms.py

from django import forms
from .models import Product,Category

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
            'status',
            'quantity',
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
            
            # 3. Campo 'status': Select para choices
            'status': forms.Select(
                attrs={
                    'class': SELECT_CLASSES,
                    'required': True
                }
            ),
            
            # 4. Campo 'quantity': NumberInput para Inteiros
            'quantity': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Quantidade',
                    'min': 0 # Adiciona a restrição min="0" diretamente
                }
            ),
            
            # 5. Campos de Valor (Cost e Sale_value): NumberInput para Decimais
            'cost': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Valor de Custo (R$)',
                    'min': 0,
                    'step': '0.01' # Para permitir valores decimais
                }
            ),
            'sale_value': forms.NumberInput(
                attrs={
                    'class': INPUT_CLASSES,
                    'placeholder': 'Valor de Venda (R$)',
                    'min': 0,
                    'step': '0.01'
                }
            ),
            
            # 6. Campo 'observation': Textarea para textos longos
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