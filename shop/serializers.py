from rest_framework import serializers
from .models import Category, Product, ProductImage, Book, BookImage, Wishlist

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImage
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = '__all__'
