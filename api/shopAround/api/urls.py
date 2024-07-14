from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, StoresViewSet, PriceReportViewSet, FavouriteProductsViewSet, UsersViewSet, CategoriesViewSet
from .converters import FloatConverter
from . import views
from api.utils.views import error_400, error_404 , error_500

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'stores', StoresViewSet)
router.register(r'prices', PriceReportViewSet)
router.register(r'favourites', FavouriteProductsViewSet)
router.register(r'users', UsersViewSet)
router.register(r'categories', CategoriesViewSet)


register_converter(FloatConverter, 'float')

urlpatterns = [
    path('', views.index, name="index"),
    path('', include(router.urls)),
    path('price-report/<int:product_id>/<float:lat>/<float:lon>/<int:rad>/', views.price_report, name='price_report'),
    path('stores/<float:lat>/<float:lon>/', views.local_stores, name='local_stores'),
    path('users/<int:user_id>/favourites/', views.favourites, name='favourites'),
    path('categories/<int:category_id>/products/', views.products_by_category, name='products_by_category')
]

handler400 = error_400
handler404 = error_404
handler500 = error_500