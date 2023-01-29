from django.db import models
from simple_history.models import HistoricalRecords
from apps.base.models import BaseModel


class MeasureUnit(BaseModel):
    description = models.CharField('Descripción', max_length=50, blank=False, null=False, unique=True)

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'

    def __str__(self):
        return self.description


class CategoryProduct(BaseModel):
    description = models.CharField('Descripcion', max_length=50, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = 'Categoría de producto'
        verbose_name_plural = 'Categorías de productos'

    def __str__(self):
        return self.description


class Indicator(BaseModel):
    discount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Indicador de oferta')

    class Meta:
        verbose_name = 'Indicador de oferta'
        verbose_name_plural = 'Indicadores de ofertas'

    def __str__(self):
        return f'Oferta de la categoría {self.category_product} : {self.discount_value}%'


class Product(BaseModel):
    name = models.CharField('Nombre de producto', max_length=150, unique=True, blank=False, null=False)
    description = models.TextField('Descripción del producto', blank=False, null=False)
    image = models.ImageField('Imagen del producto', upload_to='products/', blank=True, null=True)
    measure_unit = models.ForeignKey(MeasureUnit, on_delete=models.CASCADE, verbose_name='Unidad de Medida', null=True)
    category_product = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE, verbose_name='Categoria de Producto', null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.name