from rest_framework import generics, filters
from .models import Category, Product, ProductImage, Book, BookImage, Wishlist
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer, BookSerializer, BookImageSerializer, WishlistSerializer

class CategoryListCreateView(generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field=['id']

class ProductListCreateView(generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'status', 'category__name']
    lookup_field=['id']
class BookListCreateView(generics.ListAPIView,generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'products__name']
    lookup_field=['id']
class WishlistListCreateView(generics.ListCreateAPIView,generics.RetrieveAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'product__name']
    lookup_field=['id']