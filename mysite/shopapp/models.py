"""
Модуль models.py содержит определения моделей Django, которые представляют основные
компоненты интернет-магазина.

Этот модуль включает следующие модели:
- Tag: представляет теги, которые могут быть присвоены продуктам в интернет-магазине.
- Category: представляет категории товаров в интернет-магазине.
- Product: представляет товары, которые можно продавать в интернет-магазине.
- Discount: представляет скидки на определенные товары в интернет-магазине.
- Review: представляет отзывы пользователей о продуктах в интернет-магазине.
- ProductCharacteristic: представляет характеристики товаров.
- ProductImage: представляет изображения товаров в интернет-магазине.
- OrderStatus: представляет статусы заказов в интернет-магазине.
- DeliveryType: представляет способы доставки в интернет-магазине.
- PaymentType: представляет способы оплаты в интернет-магазине.
- Order: представляет заказы, созданные в интернет-магазине.
"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


def product_preview_directory_path(instance: "Product", filename: str):
    """
    Возвращает путь для загрузки предварительного просмотра продукта.
    """
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


def product_images_directory_path(instance: "ProductImage", filename: str):
    """
    Возвращает путь для загрузки изображения продукта.
    """
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


def category_images_directory_path(instance: "Category", filename: str):
    """
    Возвращает путь для загрузки изображения категории.
    """
    return "category/category_{pk}/images/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class Tag(models.Model):
    """
    Модель Tag представляет теги, которые могут быть присвоены продуктам в интернет-магазине.
    """

    name = models.CharField(max_length=100)


class Category(models.Model):
    """
    Модель Category представляет категорию товаров в интернет-магазине.
    """

    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=category_images_directory_path)
    parent = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='children')
    is_parent = models.BooleanField(default=False)


class Product(models.Model):
    """
    Модель Product представляет товар, который можно продавать в интернет-магазине.
    """

    title = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    fullDescription = models.TextField(null=False, blank=True, db_index=True)
    price = models.FloatField(default=0)
    date = models.DateTimeField(default=timezone.now)
    archived = models.BooleanField(default=False)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    freeDelivery = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tag, related_name="products")
    count = models.PositiveIntegerField(default=0)
    rating = models.FloatField(null=True, blank=True, default=0)
    reviews_count = models.PositiveIntegerField(default=0)
    popular = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)
    banner = models.BooleanField(default=False)

    def formatted_created_at(self):
        """
        Возвращает дату и время создания товара в формате 'YYYY-MM-DD HH:MM'.
        """
        return self.date.strftime('%Y-%m-%d %H:%M')

    def calculate_reviews_count(self):
        """
        Вычисляет общее количество отзывов о товаре.
        """
        return self.reviews.count()

    def average_rating(self):
        """
        Вычисляет среднюю оценку товара на основе отзывов.
        """
        avg_rating = self.reviews.aggregate(avg_rating=Avg('rate')).get('avg_rating')
        return avg_rating


class Discount(models.Model):
    """
       Модель Discount представляет скидку на определенный товар в интернет-магазине.
    """

    product = models.OneToOneField(Product, on_delete=models.CASCADE, primary_key=True)
    salePrice = models.FloatField()
    dateFrom = models.DateField()
    dateTo = models.DateField()


class Review(models.Model):
    """
    Модель Review представляет отзывы пользователей о продуктах в интернет-магазине.
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(default=timezone.now)
    email = models.EmailField(null=True, blank=True)

    def formatted_created_at(self):
        """
        Возвращает дату и время создания отзыва в формате 'YYYY-MM-DD HH:MM'.
        """
        return self.date.strftime('%Y-%m-%d %H:%M')


@receiver(post_save, sender=Review)
def update_product_fields(sender, instance, **kwargs):
    product = instance.product
    product.reviews_count = product.calculate_reviews_count()
    product.rating = product.average_rating()
    product.save()


class ProductCharacteristic(models.Model):
    """
    Модель ProductCharacteristic представляет характеристики товаров.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100, default=None)


class ProductImage(models.Model):
    """
        Модель ProductImage представляет изображения товаров в интернет-магазине.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)


class OrderStatus(models.Model):
    """
    Модель OrderStatus представляет статус заказа в интернет-магазине.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление статуса заказа.
        """
        return self.name


class DeliveryType(models.Model):
    """
    Модель DeliveryType представляет способ доставки в интернет-магазине.
    """

    name = models.CharField(max_length=100)
    price = models.FloatField(default=0)

    def __str__(self):
        """
        Возвращает строковое представление способа доставки.
        """
        return self.name


class PaymentType(models.Model):
    """
    Модель PaymentType представляет способ оплаты в интернет-магазине.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Возвращает строковое представление способа оплаты.
        """
        return self.name


class Order(models.Model):
    """
        Модель Order представляет заказ, созданный в интернет-магазине.
    """

    createdAt = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_orders')
    products = models.ManyToManyField(Product, related_name="product_orders")
    status = models.ForeignKey(OrderStatus, on_delete=models.PROTECT, null=True)
    deliveryType = models.ForeignKey(DeliveryType, on_delete=models.PROTECT, null=True)
    paymentType = models.ForeignKey(PaymentType, on_delete=models.PROTECT, null=True)
    totalCost = models.FloatField(default=0)

    class Meta:
        ordering = ['-createdAt']

    def formatted_created_at(self):
        """
        Возвращает дату и время создания заказа в формате 'YYYY-MM-DD HH:MM'.
        """
        return self.createdAt.strftime('%Y-%m-%d %H:%M')
