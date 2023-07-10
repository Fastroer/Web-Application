from django.urls import reverse
from django_filters.compat import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Category, Tag
from .serializers import CategorySerializer, TagSerializer


class CategoryListAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('category-list')

    def test_get_category_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = Category.objects.filter(is_parent=True)
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, serializer.data)


class TagsAPIViewTest(TestCase):
    def setUp(self):
        self.url = '/api/tags'

    def test_get_tag_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, serializer.data)
