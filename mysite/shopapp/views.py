"""
Этот файл содержит представления (views) Django, которые обрабатывают HTTP-запросы
и возвращают HTTP-ответы. Каждое представление определяет, как будет обрабатываться
конкретный тип запроса (GET, POST, etc.) и какие данные будут возвращены в ответе.
"""

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, Tag, Review, Discount, Order, OrderStatus, PaymentType, DeliveryType
from .serializers import CategorySerializer, CatalogResponseSerializer, TagSerializer, ProductSerializer, \
    ProductDetailsSerializer, ReviewSerializer, DiscountSerializer, SaleResponseSerializer, CartItemSerializer, \
    CartGETSerializer, OrderSerializer
from rest_framework.filters import OrderingFilter
from django.db.models import Avg, Q
from authapp.models import Cart, CartItem


class CategoryListAPIView(generics.ListAPIView):
    """
    Класс представления для получения списка категорий.

    Сериализует и возвращает список категорий, которые являются родительскими.
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Получает и возвращает список категорий, которые являются родительскими.
        """
        return Category.objects.filter(is_parent=True)


class TagsAPIView(generics.ListAPIView):
    """
    Класс представления для получения списка тегов.

    Сериализует и возвращает список всех тегов.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductAPIView(generics.RetrieveAPIView):
    """
    Класс представления для получения информации о продукте.

    Сериализует и возвращает информацию о продукте с заданным идентификатором.
    """
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Получает и возвращает список всех продуктов, исключая архивированные, с указанным идентификатором.
        """
        queryset = super().get_queryset()
        return queryset.filter(archived=False, id=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        """
        Получает и возвращает информацию о продукте с заданным идентификатором.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CatalogAPIView(generics.ListAPIView):
    """
    Класс представления для получения списка продуктов в каталоге.

    Сериализует и возвращает список продуктов с возможностью фильтрации, сортировки и пагинации.
    """

    filter_backends = [OrderingFilter]
    serializer_class = CatalogResponseSerializer

    def filter_queryset(self, queryset):
        """
        Фильтрует и сортирует список продуктов согласно параметрам запроса.
        """
        name_param = self.request.GET.get('filter[name]')
        min_price_param = self.request.GET.get('filter[minPrice]')
        max_price_param = self.request.GET.get('filter[maxPrice]')
        freeDelivery_param = self.request.GET.get('filter[freeDelivery]')
        available_param = self.request.GET.get('filter[available]')
        sort_param = self.request.GET.get('sort')
        sort_type_param = self.request.GET.get('sortType')
        tags_param = self.request.GET.getlist('tags[]')

        if name_param:
            queryset = queryset.filter(title__icontains=name_param)
        if min_price_param:
            queryset = queryset.filter(price__gte=min_price_param)
        if max_price_param:
            queryset = queryset.filter(price__lte=max_price_param)
        if freeDelivery_param is not None:
            freeDelivery = freeDelivery_param.lower() == 'false'
            if freeDelivery:
                queryset = queryset.filter(
                    Q(freeDelivery=True) | Q(freeDelivery=False) | Q(freeDelivery__isnull=True))
            else:
                queryset = queryset.filter(Q(freeDelivery=True) | Q(freeDelivery__isnull=True))
        if available_param:
            queryset = queryset.filter(available=available_param.lower() == 'true')
        if tags_param:
            queryset = queryset.filter(tags__in=tags_param)

        if sort_param:
            sort_fields = [sort_field.strip() for sort_field in sort_param.split(',')]
            sort_types = [sort_type.strip() for sort_type in sort_type_param.split(',')]
            ordering = []

            for field, sort_type in zip(sort_fields, sort_types):
                if sort_type == 'dec':
                    ordering.append(field)
                elif sort_type == 'inc':
                    ordering.append('-' + field)

            queryset = queryset.order_by(*ordering)

        return queryset

    def get_queryset(self):
        """
        Возвращает queryset, содержащий список продуктов.
        """
        queryset = Product.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Возвращает список продуктов в каталоге.
        """
        queryset = self.filter_queryset(self.get_queryset())

        paginator = Paginator(queryset, 10)
        page_number = request.GET.get('currentPage')
        page_obj = paginator.get_page(page_number)

        serializer = ProductSerializer(page_obj, many=True)
        data = {
            'items': serializer.data,
            'currentPage': page_obj.number,
            'lastPage': paginator.num_pages,
        }
        return Response(data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ViewSet):
    """
    ViewSet для создания отзывов о продукте.
    """

    def create(self, request, pk=None):
        """
        Создает новый отзыв о продукте.

        Параметры:
        - pk (int): Первичный ключ продукта, для которого создается отзыв.

        Возвращает:
        - Response: Ответ, содержащий созданный отзыв и связанную информацию.
        """
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Продукт не найден.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = Review(
                product=product,
                author=serializer.validated_data['author'],
                text=serializer.validated_data['text'],
                rate=serializer.validated_data['rate'],
                email=serializer.validated_data['email']
            )
            review.save()

            product.reviews_count = product.reviews.count()
            product.rating = product.reviews.aggregate(avg_rating=Avg('rate')).get('avg_rating')
            product.save()

            reviews = product.reviews.all()
            reviews_serializer = ReviewSerializer(reviews, many=True)

            return Response(reviews_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PopularProductsAPIView(generics.ListAPIView):
    """
    Представление для получения популярных продуктов.
    """

    queryset = Product.objects.filter(popular=True)
    serializer_class = ProductSerializer


class LimitedProductsAPIView(generics.ListAPIView):
    """
    Представление для получения ограниченных продуктов.
    """

    queryset = Product.objects.filter(limited=True)
    serializer_class = ProductSerializer


class BannersAPIView(generics.ListAPIView):
    """
    Представление для получения продуктов-баннеров.
    """

    queryset = Product.objects.filter(banner=True)[:3]
    serializer_class = ProductSerializer


class DiscountedProductsAPIView(generics.ListAPIView):
    """
    Представление для получения продуктов со скидкой с пагинацией.
    """

    serializer_class = SaleResponseSerializer
    queryset = Discount.objects.all()

    def get(self, request, *args, **kwargs):
        """
        Получает список продуктов со скидкой с пагинацией.

        Параметры:
        - request: Объект запроса.
        - args: Дополнительные аргументы.
        - kwargs: Дополнительные именованные аргументы.

        Возвращает:
        - Response: Ответ, содержащий список продуктов со скидкой с пагинацией.
        """
        paginator = Paginator(self.queryset.order_by('product'), 10)
        page_number = request.GET.get('currentPage')
        page_obj = paginator.get_page(page_number)

        serializer = DiscountSerializer(page_obj, many=True)
        data = {
            'items': serializer.data,
            'currentPage': page_obj.number,
            'lastPage': paginator.num_pages,
        }
        return Response(data, status=status.HTTP_200_OK)


class BasketAPIView(APIView):
    """
    Класс представления для работы с корзиной пользователя.
    """

    def get(self, request):
        """
        Возвращает корзину пользователя.
        """
        user = request.user
        cart = Cart.objects.get(user=user)
        items = cart.items.all()
        products = [item.product for item in items]
        serializer = CartGETSerializer(products, many=True, context={'cart': cart})
        return Response(serializer.data)

    def post(self, request):
        """
        Добавляет товар в корзину пользователя.
        """
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['id']
            count = serializer.validated_data['count']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Invalid product ID'}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            cart, created = Cart.objects.get_or_create(user=user)

            try:
                item = cart.items.get(product=product)
                item.count += count
                item.save()
            except CartItem.DoesNotExist:
                item = CartItem.objects.create(cart=cart, product=product, count=count)

            items = cart.items.all()
            products = [item.product for item in items]
            serializer = CartGETSerializer(products, many=True, context={'cart': cart})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """
        Удаляет товар из корзины пользователя.
        """
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
            product_id = request.data.get('id')
            count = request.data.get('count', 1)

            if product_id is None:
                return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

            cart_item = cart.items.filter(product=product).first()

            if cart_item:
                new_count = cart_item.count - int(count)
                if new_count < 0:
                    return Response({'error': 'Count cannot be negative.'}, status=status.HTTP_400_BAD_REQUEST)
                elif new_count == 0:
                    cart_item.delete()
                else:
                    cart_item.count = new_count
                    cart_item.save()

            items = cart.items.all()
            products = [item.product for item in items]
            serializer = CartGETSerializer(products, many=True, context={'cart': cart})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found.'}, status=status.HTTP_404_NOT_FOUND)


class OrderAPIView(APIView):
    """
    Представление для работы с заказами.
    """

    def get(self, request):
        """
        Получает список всех заказов.

        Возвращает:
        - Response: Ответ с данными о заказах.
        """
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Создает новый заказ.

        Параметры:
        - request: Запрос, содержащий информацию о товарах.

        Возвращает:
        - Response: Ответ с данными о созданном заказе.
        """
        products = request.data

        order = Order.objects.create(user=request.user)

        for product_data in products:
            product = Product.objects.get(id=product_data['id'])

            order.products.add(product)

        order.deliveryType = get_object_or_404(DeliveryType, id=3)
        order.paymentType = get_object_or_404(PaymentType, id=3)
        order.status = get_object_or_404(OrderStatus, id=7)
        order.save()

        serializer = OrderSerializer(order)
        data = serializer.data
        data['orderId'] = order.id

        user = request.user
        cart = user.cart
        cart.items.all().delete()

        return Response(data, status=status.HTTP_201_CREATED)


class OrderDetailView(generics.RetrieveAPIView):
    """
    Представление для работы с конкретным заказом.
    """

    def get(self, request, pk):
        """
        Получает информацию о конкретном заказе.

        Параметры:
        - request: Запрос.
        - pk (int): Первичный ключ заказа.

        Возвращает:
        - Response: Ответ с данными о заказе.
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        """
        Обновляет информацию о конкретном заказе.

        Параметры:
        - request: Запрос, содержащий данные для обновления заказа.
        - pk (int): Первичный ключ заказа.

        Возвращает:
        - Response: Ответ с обновленными данными о заказе.
        """
        payload_data = request.data
        try:
            order = Order.objects.get(pk=pk)
            total_cost = 0
            products = payload_data.get('products', [])
            for product_data in products:
                price = product_data.get('price', 0)
                count = product_data.get('count', 0)
                total_cost += price * count

            if payload_data.get('deliveryType') == 'express':
                delivery_type = DeliveryType.objects.get(pk=1)
                order.deliveryType = delivery_type
                total_cost += delivery_type.price
            else:
                delivery_type = DeliveryType.objects.get(pk=2)
                order.deliveryType = delivery_type
                total_cost += delivery_type.price

            if payload_data.get('paymentType') == 'someone':
                order.paymentType = PaymentType.objects.get(pk=2)
            else:
                order.paymentType = PaymentType.objects.get(pk=1)

            order.status = OrderStatus.objects.get(pk=1)
            order.totalCost = total_cost
            order.save()

            request.session['orderId'] = order.id

            return Response({'orderId': order.id}, status=status.HTTP_201_CREATED)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PaymentView(generics.RetrieveAPIView):
    """
    Представление для оплаты заказа.
    """

    def get(self, request, pk):
        """
        Обрабатывает оплату заказа.

        Параметры:
        - request: Запрос.
        - pk (int): Первичный ключ заказа.

        Возвращает:
        - Response: Ответ с результатом оплаты.
        """
        order_id = request.session.pop('orderId', None)
        if order_id:
            try:
                Order.objects.get(pk=order_id)
                return Response({'message': 'Оплата прошла успешно.'})
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk):
        """
        Обновляет статус заказа после оплаты.

        Параметры:
        - request: Запрос.
        - pk (int): Первичный ключ заказа.

        Возвращает:
        - Response: Ответ с обновленным статусом заказа.
        """
        order_id = request.session.get('orderId')
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                order.status = OrderStatus.objects.get(pk=3)
                order.save()
                return Response({'message': 'Статус заказа успешно обновлен.'})
            except Order.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
