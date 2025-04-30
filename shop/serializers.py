from rest_framework import serializers
from .models import *


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'



class BoxsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxImage
        fields = '__all__'



class BoxSerializer(serializers.ModelSerializer):
    images = BoxsImageSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    category=serializers.SerializerMethodField()
    class Meta:
        model = Box
        fields = '__all__'

    def get_category(self,obj):
        return obj.category.name





class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategorySerializerOnly(serializers.ModelSerializer):
    category_product= ProductSerializer(many=True ,read_only=True)
    category_box= BoxSerializer(many=True ,read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'





class WishlistSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = "__all__"

    def get_content_object(self, obj):
        if isinstance(obj.content_object, Product):
            return ProductSerializer(obj.content_object).data
        elif isinstance(obj.content_object, Box):
            return BoxSerializer(obj.content_object).data
        return None




class CartItemSerializer(serializers.ModelSerializer):
    content_object = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = "__all__"

    def get_content_object(self, obj):
        if isinstance(obj.content_object, Product):
            return ProductSerializer(obj.content_object).data
        elif isinstance(obj.content_object, Box):
            return BoxSerializer(obj.content_object).data
        return None


class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = "__all__"


