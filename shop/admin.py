from django.contrib import admin

from django.contrib import admin
from .models import (
    Category, Product, ProductImage,
    Box, BoxImage,
    Wishlist, Cart, CartItem
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'status', 'category')
    list_filter = ('status', 'category')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]


class BoxImageInline(admin.TabularInline):
    model = BoxImage
    extra = 1


class BoxAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)
    filter_horizontal = ('products',)
    inlines = [BoxImageInline]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'content_object')
    list_filter = ('user',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


class CartAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [CartItemInline]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Box, BoxAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Cart, CartAdmin)
