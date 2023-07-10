from rest_framework import serializers
from .models import Product, Category, Review, Tag, ProductCharacteristic, Discount
from authapp.models import CartItem, Cart
from .models import Order


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_image(self, obj):
        if obj.image:
            src = obj.image.url
            alt = obj.description
        else:
            src = "/media/Отсутствие.png"
            alt = "Изображение отсутствует"
        return {
            'src': src,
            'alt': alt
        }

    def get_subcategories(self, obj):
        subcategories = obj.children.all()
        serializer = CategorySerializer(subcategories, many=True)
        return serializer.data


class SpecificationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCharacteristic
        fields = ('name', 'value')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('author', 'email', 'text', 'rate', 'date')


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_images(self, obj):
        preview = str(obj.preview)
        if preview:
            return [{'src': "/media/" + preview, 'alt': 'Preview Image'}]
        else:
            return [{'src': '/media/Отсутствие.png', 'alt': 'Изображение отсутствует'}]

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rate for review in reviews)
            return total_rating / reviews.count()
        return 0

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title', 'description',
            'freeDelivery', 'images', 'tags', 'reviews', 'rating',
        ]


class CatalogResponseSerializer(serializers.Serializer):
    items = ProductSerializer(many=True)
    currentPage = serializers.IntegerField()
    lastPage = serializers.IntegerField()


class ProductDetailsSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationsSerializers(many=True)
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    def get_images(self, obj):
        preview = str(obj.preview)
        if preview:
            return [{'src': "/media/" + preview, 'alt': 'Preview Image'}]
        else:
            return [{'src': '/media/Отсутствие.png', 'alt': 'Изображение отсутствует'}]

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rate for review in reviews)
            return total_rating / reviews.count()
        return None

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription',
            'freeDelivery', 'images', 'tags', 'reviews', 'specifications', 'rating',
        ]


class DiscountSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='product.id', read_only=True)
    title = serializers.CharField(source='product.title', read_only=True)
    price = serializers.FloatField(source='product.price', read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        product = obj.product
        preview = str(product.preview)
        if preview:
            return [{'src': "/media/" + preview, 'alt': 'Preview Image'}]
        else:
            return [{'src': '/media/Отсутствие.png', 'alt': 'Изображение отсутствует'}]

    class Meta:
        model = Discount
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images']


class SaleResponseSerializer(serializers.Serializer):
    items = DiscountSerializer(many=True)
    currentPage = serializers.IntegerField()
    lastPage = serializers.IntegerField()


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1)


class CartGETSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    count = serializers.SerializerMethodField()

    def get_images(self, obj):
        preview = str(obj.preview)
        if preview:
            return [{'src': "/media/" + preview, 'alt': 'Preview Image'}]
        else:
            return [{'src': '/media/Отсутствие.png', 'alt': 'Изображение отсутствует'}]

    def get_reviews(self, obj):
        return obj.reviews.count()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            total_rating = sum(review.rate for review in reviews)
            return total_rating / reviews.count()
        return 0

    def get_count(self, obj):
        cart = self.context['cart']
        try:
            cart_item = cart.items.get(product=obj)
            return cart_item.count
        except CartItem.DoesNotExist:
            return 0

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'price', 'date', 'title', 'description',
            'freeDelivery', 'images', 'tags', 'reviews', 'rating', 'count',
        ]


class OrderSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    products = ProductSerializer(many=True)
    deliveryType = serializers.StringRelatedField()
    paymentType = serializers.StringRelatedField()
    status = serializers.StringRelatedField()

    products_data = serializers.ListField(write_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'createdAt', 'totalCost', 'fullName', 'email', 'phone', 'deliveryType', 'paymentType', 'status',
            'city', 'address', 'products', 'products_data',
        ]

    def get_fullName(self, obj):
        return obj.user.profile.fullName

    def get_email(self, obj):
        return obj.user.profile.email

    def get_phone(self, obj):
        return obj.user.profile.phone

    def get_address(self, obj):
        return obj.user.profile.address

    def get_city(self, obj):
        return obj.user.profile.city

    def create(self, validated_data):
        products_data = validated_data.pop('products_data', [])

        order = Order.objects.create(**validated_data)

        for product_data in products_data:
            product = Product.objects.get(id=product_data['id'])
            count = product_data.get('count', 1)

            order.products.add(product, through_defaults={'count': count})

        return order
