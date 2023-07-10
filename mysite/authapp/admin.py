from django.contrib import admin
from .models import UserProfile, Cart, CartItem


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'fullName', 'phone', 'email', 'city', 'address')
    search_fields = ('user__username', 'user__email', 'fullName', 'phone', 'email', 'city', 'address')


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'count')
    search_fields = ('cart__user__username', 'cart__user__email', 'product__title')
