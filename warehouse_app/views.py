from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, UpdateView, DetailView, ListView, CreateView, DeleteView
from .models import ProductModel, CategoryModel, Profit
from .forms import *
from django.urls import reverse_lazy, reverse
from django.views import View
import datetime
from django.shortcuts import render
from django.db.models import Count, Avg, Q


class StartView(TemplateView):
    """Представление стартовой страницы"""
    template_name = 'start.html'


class AuthorLogoutView(LogoutView):
    """Представление для выхода пользователя из учетной записи"""
    next_page = '/'


class AuthorLoginView(LoginView):
    """Представление для входа пользователя в учетную запись"""
    template_name = 'login.html'


class ProfitView(ListView):
    """Представление для вывода прибыли по месяцам"""
    model = Profit
    template_name = 'profit_list.html'
    ordering = ['date']


class AllCategoryView(ListView):
    """Представление для вывода категорий товаров"""
    model = CategoryModel
    template_name = 'category_list.html'
    ordering = ['group']


class CategoryProductView(ListView):
    """Представление для вывода товаров определенной категории"""
    model = ProductModel
    template_name = 'category_product.html'
    ordering = ['products']

    def get(self, request, *args, **kwargs):
        """Если форма поиска пустая, то при запросе выводятся все товары категории,
         иначе происходит фильтрация по запросу поиска"""
        if request.GET.get('q'):
            result = ProductModel.objects.filter(group_product_id=self.kwargs.get('pk')).\
                filter(products__icontains=request.GET.get('q'))
        else:
            result = ProductModel.objects.filter(group_product_id=self.kwargs.get('pk'))
        return render(request, 'category_product.html', context={'object_list': result})


class OneProductView(DetailView):
    """Представление для вывода одного товара"""
    model = ProductModel
    template_name = 'one_product.html'


class ProductRecordView(CreateView):
    """Представление для добавления товара """
    success_url = reverse_lazy('new_product')
    model = ProductModel
    template_name = 'new_product.html'
    fields = ['group_product', 'products', 'article', 'comment', 'price_zakupka',
              'price', 'spd_count', 'mos_count', 'file']


class ProductUpdateView(UpdateView):
    """Представление для редактирования товара, редирект на страницу товара, который редактируем"""
    model = ProductModel
    template_name = 'product_edit.html'
    fields = ['products', 'article', 'comment', 'price_zakupka', 'price', 'group_product', 'file']

    def get_success_url(self):
        pk = self.kwargs["pk"]
        group = self.kwargs['group_product_id']
        return reverse('one_product', kwargs={'group_product_id': group, 'pk': pk})


class ProductDeleteView(DeleteView):
    """Представление для удаления продукта из базы данных"""
    model = ProductModel
    template_name = 'product_delete.html'

    def get_success_url(self):
        pk = self.kwargs['group_product_id']
        return reverse('category_product', kwargs={'pk': pk})


class MoscowUpdateView(UpdateView):
    """Представление для изменения количества товара на складе в Москве"""
    model = ProductModel
    template_name = 'delete_moscow.html'
    fields = ['mos_count']

    def get_success_url(self):
        pk = self.kwargs['group_product_id']
        return reverse('category_product', kwargs={'pk': pk})


class SpbUpdateView(UpdateView):
    """Представление для изменения количества товара на складе в Санкт-Петербурге"""
    model = ProductModel
    template_name = 'delete_spb.html'
    fields = ['spd_count']

    def get_success_url(self):
        pk = self.kwargs['group_product_id']
        return reverse('category_product', kwargs={'pk': pk})


class CategoryRecordView(CreateView):
    """Представление для добавления категории """
    success_url = reverse_lazy('category')
    model = CategoryModel
    template_name = 'new_category.html'
    fields = '__all__'


def statistics(request):
    """Функция просмотра статиски проданных товаров в интервале дат, указанных пользователем"""
    if request.method == 'GET':
        form = DateForms()
        return render(request, 'statistics.html', {'form': form})

    if request.method == 'POST':
        start_date = request.POST.get('first_date')
        end_date = request.POST.get('second_date')
        product_sale = ProductModel.objects.annotate(
            num_sale=Count('statistics', filter=Q(statistics__created_at__range=
                                                  [start_date, end_date]))).order_by('-num_sale')[:10]
        form = DateForms()
        return render(request, 'statistics.html', {'object_list': product_sale, 'form': form})
