from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType

from .models import *
from .serializers import *


# ---------- Product ----------
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# ---------- Box ----------
class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BookSerializer

class BoxDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'id'


# ---------- Category ----------
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


# ---------- Wishlist ----------
class WishlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        model_name = self.request.data.get("content_type")
        object_id = self.request.data.get("object_id")

        try:
            content_type = ContentType.objects.get(model=model_name.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError({"content_type": "Invalid model name"})

        serializer.save(user=user, content_type=content_type, object_id=object_id)


class WishlistDetailView(generics.RetrieveDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    lookup_field = 'id'


# ---------- Cart ----------
class CartListCreateView(generics.ListAPIView):
    serializer_class = CartSerializer
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    lookup_field = 'id'


# ---------- CartItem ----------
class CartItemCreateView(APIView):
    def post(self, request):
        data = request.data.copy()
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        model_name = data.get("content_type")
        object_id = data.get("object_id")
        quantity = data.get("quantity", 1)
  
        try:
            content_type = ContentType.objects.get(model=model_name.lower())
            model_class = content_type.model_class()
            content_object = model_class.objects.get(id=object_id)
        except (ContentType.DoesNotExist, model_class.DoesNotExist):
            return Response({'error': 'Invalid content object'}, status=status.HTTP_400_BAD_REQUEST)
        item = CartItem.objects.create(
            cart=cart,
            content_type=content_type,
            object_id=object_id,
            quantity=quantity
        )
        serializer = CartItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self,request):
        
        