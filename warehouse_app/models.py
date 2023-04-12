from django.contrib.auth.models import User
from django.db import models
import datetime
from django.contrib.postgres.indexes import GinIndex
from django.core.exceptions import ObjectDoesNotExist


def function_profit(total_profit):
    dates = datetime.datetime.now().strftime("%m/%Y")
    try:
        one = Profit.objects.get(date=dates)
        one.profit += total_profit
        one.save()
    except ObjectDoesNotExist:
        Profit.objects.create(profit=0, date=dates)
        one = Profit.objects.get(date=dates)
        one.profit += total_profit
        one.save()


class Profit(models.Model):
    profit = models.IntegerField(default=0, verbose_name='прибыль')
    date = models.CharField(default='profit', max_length=30, verbose_name='месяц отчетности')


class CategoryModel(models.Model):
    """Модель категории товаров"""
    group = models.CharField(default='без группы', max_length=100, verbose_name='группа товара')

    def __str__(self):
        return self.group


class ProductModel(models.Model):
    """Модель товара"""
    group_product = models.ForeignKey('CategoryModel', default=None, on_delete=models.CASCADE,
                                      verbose_name='категория товара')
    products = models.CharField(max_length=10000, verbose_name='товар')
    article = models.CharField(default=' ', max_length=100, verbose_name='артикул')
    create_at = models.CharField(default=datetime.datetime.now().date(), max_length=30,  verbose_name='дата добавления')
    comment = models.CharField(default=' ', max_length=100, verbose_name='описание')
    price_zakupka = models.IntegerField(verbose_name='цена закупочная')
    price = models.IntegerField(verbose_name='цена')
    spd_count = models.IntegerField(default=0, verbose_name='колличество СПБ')
    mos_count = models.IntegerField(default=0, verbose_name='колличество МОСКВА')
    file = models.FileField(default='files/no_products.jpg', blank=True, null=True, upload_to='files/', verbose_name='фото товара')

    class Meta:
        indexes = [GinIndex(fields=['products'])]

    @classmethod
    def from_db(cls, db, field_names, values):
        """Методы для отслеживания изменений в поле формы,
         при изменении вычисляется разница значений и записывается в БД"""
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        """Функция для отслеживания изменения значения полей 'spd_count' и 'mos_count',
         формирования объекта модели статистики"""
        if not self._state.adding:
            new_val_spb = self.spd_count
            old_val_spb = self._loaded_values['spd_count']
            new_val_msk = self.mos_count
            old_val_msk = self._loaded_values['mos_count']
            profit = self._loaded_values['price'] - self._loaded_values['price_zakupka']

            if old_val_spb != new_val_spb:
                if new_val_spb < old_val_spb:
                    total_profit = (old_val_spb - new_val_spb) * profit
                    for _ in range(old_val_spb - new_val_spb):
                        Statistics.objects.create(product_id=self.id)
                    function_profit(total_profit=total_profit)

            elif old_val_msk != new_val_msk:
                if new_val_msk < old_val_msk:
                    total_profit = (old_val_msk - new_val_msk) * profit
                    for _ in range(old_val_msk - new_val_msk):
                        Statistics.objects.create(product_id=self.id)
                    function_profit(total_profit=total_profit)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.products


class Statistics(models.Model):
    product = models.ForeignKey('ProductModel', on_delete=models.CASCADE, verbose_name='продукт', null=True)
    created_at = models.DateField(auto_now_add=True)

