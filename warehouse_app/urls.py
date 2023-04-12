from django.contrib import admin
from django.urls import path, include
from .views import AuthorLoginView, StartView, AuthorLogoutView, \
    OneProductView, ProductRecordView, AllCategoryView, CategoryProductView, \
    ProductUpdateView, ProductDeleteView, MoscowUpdateView, SpbUpdateView, CategoryRecordView, ProfitView, statistics
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', StartView.as_view(), name='start'),  # стартовая
                  path('login/', AuthorLoginView.as_view(), name='login'),  # для входа
                  path('profit/', ProfitView.as_view(), name='profit'),
                  path('logout/', AuthorLogoutView.as_view(), name='logout'),  # для выхода
                  path('category_product/<int:group_product_id>/<int:pk>/', OneProductView.as_view(),
                       name='one_product'),  # одного товара
                  path('category/', AllCategoryView.as_view(), name='category'),  # список категорий
                  path('new_product/', ProductRecordView.as_view(), name='new_product'),  # добавление товара
                  path('category_product/<int:pk>/', CategoryProductView.as_view(),
                       name='category_product'),  # товары выбранной категории
                  path('category_product/<int:group_product_id>/<int:pk>/edit/', ProductUpdateView.as_view(),
                       name='product_edit'),  # редактирования товара
                  path('category_product/<int:group_product_id>/<int:pk>/delete/', ProductDeleteView.as_view(),
                       name='product_delete'),  # удаления товара
                  path('category_product/<int:group_product_id>/<int:pk>/moscow/', MoscowUpdateView.as_view(),
                       name='moscow_edit'),  # редактирование количества на складе в МСК
                  path('category_product/<int:group_product_id>/<int:pk>/spb/', SpbUpdateView.as_view(),
                       name='spb_edit'),  # редактирование количества на складе в СПБ
                  path('new_category/', CategoryRecordView.as_view(), name='new_category'),
                  path('statistics/', statistics, name='statistics')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
