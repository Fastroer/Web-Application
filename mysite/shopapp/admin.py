from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Order, Tag, ProductCharacteristic, Discount, OrderStatus, \
    PaymentType, DeliveryType


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ReviewInline(admin.TabularInline):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_parent')
    list_filter = ('is_parent',)
    search_fields = ('title',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'available', 'popular', 'limited', 'banner')
    list_filter = ('category', 'available', 'popular', 'limited', 'banner')
    search_fields = ('title', 'description')
    inlines = [ProductImageInline, ReviewInline]


@admin.register(ProductCharacteristic)
class ProductCharacteristicAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    list_filter = ('product',)
    search_fields = ('product__title', 'name')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rate', 'date')
    list_filter = ('product', 'rate')
    search_fields = ('product__title', 'author')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'deliveryType', 'paymentType', 'totalCost', 'formatted_created_at')
    list_filter = ('status', 'deliveryType', 'paymentType')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('formatted_created_at',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('product', 'salePrice', 'dateFrom', 'dateTo')
    list_filter = ('dateFrom', 'dateTo')
    search_fields = ('product__title',)


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DeliveryType)
class DeliveryTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)


admin.site.register(ProductImage)
