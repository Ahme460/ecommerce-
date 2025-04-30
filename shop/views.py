from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import AllowAny ,IsAuthenticated
from .models import *
from .serializers import *
from .utls import total

# ---------- Product ----------
class ProductListCreateView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


# ---------- Box ----------
class BoxListCreateView(generics.ListCreateAPIView):
    queryset = Box.objects.all().prefetch_related('products')
    serializer_class = BoxSerializer

class BoxDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all().prefetch_related('products')
    serializer_class = BoxSerializer
    lookup_field = 'id'


# ---------- Category ----------
class CategoryListCreateView(generics.ListAPIView):
    queryset = Category.objects.all().prefetch_related('category_box','category_product')
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all().prefetch_related('category_box','category_product')
    serializer_class = CategorySerializerOnly
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
# class CartListCreateView(generics.ListAPIView):
#     serializer_class = CartSerializer
#     def get_queryset(self):
#         return Cart.objects.filter(user=self.request.user)


class CartListCreateView(APIView):
    
    permission_classes=[IsAuthenticated]
    def get(self,request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartItemSerializer(cart.items.all(), many=True)
        return Response(serializer.data)
    




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
        pass


class CartSession(APIView):
    permission_classes=[AllowAny]
    
    def post(self,request):
        item_type=request.data.get('type',None)
        id_item=request.data.get('id',None)
        quantity =request.data.get('quantity',None)
        cart = request.session.get("cart", {})
        key = f"{item_type}_{id_item}"
        if key in cart:
            cart[key]["quantity"] += quantity
        else:
            cart[key] = {"quantity": quantity}
        request.session["cart"] = cart
        return Response({"message": "Added to cart", "cart": cart})


class ViewCartAPIView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        cart = request.session.get("cart", {})
        result = []

        for key, value in cart.items():
            item_type, item_id = key.split("_")
            if item_type == "product":
                item = Product.objects.filter(id=item_id).first()
                serializer = ProductSerializer(item) if item else None
            elif item_type == "box":
                item = Box.objects.filter(id=item_id).first()
                serializer = BoxSerializer(item) if item else None
            else:
                serializer = None

            if serializer:
                result.append({
                    "type": item_type,
                    "data": serializer.data,
                    "quantity": value["quantity"]
                })
        total_price = total(result)
            
        return Response({
            "items": result,
            "total": total_price
        })
        