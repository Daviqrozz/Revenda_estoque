from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name

STATUS_IN_STOCK = 1
STATUS_SALED = 0

STATUS_OPTIONS = {
    (STATUS_IN_STOCK,'Em estoque'),
    (STATUS_SALED,'Vendido')
}
class Product(models.Model):
    name = models.CharField(max_length=130)
    observation = models.CharField(max_length=200,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,related_name='category',null=True)
    status = models.IntegerField(
        choices=STATUS_OPTIONS,
        default=STATUS_IN_STOCK,
        verbose_name='Status'
    )
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=10,decimal_places=2)
    sale_value = models.DecimalField(max_digits=10,decimal_places=2)
    cadastred_date = models.DateTimeField(auto_now_add=True)
    
    @property
    def profit(self):
        return self.sale_value - self.cost
    
    def __str__(self):
        return f"{self.name} | R$ {self.sale_value} | Qtd: {self.quantity}"
    
    
    
