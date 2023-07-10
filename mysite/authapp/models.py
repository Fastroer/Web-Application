"""
Модуль models.py содержит определения моделей Django, представляющих компоненты интернет-магазина.

Этот модуль включает следующие модели:
- Cart: представляет корзину пользователя с полем count для каждого товара.
- CartItem: представляет товар в корзине с полем count.
- UserProfile: представляет профиль пользователя.
"""

from django.db import models
from django.contrib.auth.models import User
from shopapp.models import Product, Order


class Cart(models.Model):
    """
    Модель Cart представляет корзину пользователя с полем count для каждого товара.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    """
    Модель CartItem представляет товар в корзине с полем count.
    """

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)


class UserProfile(models.Model):
    """
    Модель UserProfile представляет профиль пользователя.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    fullName = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)


