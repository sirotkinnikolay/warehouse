from django.contrib import admin
from .models import CategoryModel, ProductModel, Profit


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['group']


admin.site.register(CategoryModel, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['group_product', 'products', 'create_at', 'article', 'comment',
                    'file', 'price_zakupka', 'price', 'spd_count', 'mos_count']


admin.site.register(ProductModel, ProductAdmin)


class ProfitAdmin(admin.ModelAdmin):
    list_display = ['profit']


admin.site.register(Profit, ProfitAdmin)

