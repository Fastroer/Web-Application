from django.urls import path
from .views import CategoryListAPIView, CatalogAPIView, TagsAPIView, ProductAPIView, ReviewViewSet, \
    PopularProductsAPIView, LimitedProductsAPIView, BannersAPIView, DiscountedProductsAPIView, BasketAPIView, \
    OrderAPIView, OrderDetailView, PaymentView

urlpatterns = [
    path('categories', CategoryListAPIView.as_view(), name='category-list'),
    path('tags', TagsAPIView.as_view(), name='tags'),
    path('catalog', CatalogAPIView.as_view(), name='catalog'),
    path('product/<int:pk>', ProductAPIView.as_view(), name='product'),
    path('product/<int:pk>/reviews', ReviewViewSet.as_view({'post': 'create'}), name='create-review'),
    path('products/popular', PopularProductsAPIView.as_view(), name='popular-products'),
    path('products/limited', LimitedProductsAPIView.as_view(), name='limited-products'),
    path('banners', BannersAPIView.as_view(), name='banners'),
    path('sales', DiscountedProductsAPIView.as_view(), name='sales'),
    path('basket', BasketAPIView.as_view(), name='basket'),
    path('orders', OrderAPIView.as_view(), name='order'),
    path('order/<int:pk>', OrderDetailView.as_view(), name='order-detail'),
    path('payment/<int:pk>', PaymentView.as_view(), name='payment'),
]
