from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView,
    BoxListCreateView, BoxDetailView,
    CategoryListCreateView, CategoryDetailView,
    WishlistListCreateView, WishlistDetailView,
    CartListCreateView, CartDetailView,
    CartItemCreateView,
    CartSession, ViewCartAPIView
)

urlpatterns = [
    # Product
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product-detail'),

    # Box
    path('boxes/', BoxListCreateView.as_view(), name='box-list'),
    path('boxes/<int:id>/', BoxDetailView.as_view(), name='box-detail'),

    # Category
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category-detail'),

    # Wishlist
    path('wishlist/', WishlistListCreateView.as_view(), name='wishlist-list'),
    path('wishlist/<int:id>/', WishlistDetailView.as_view(), name='wishlist-detail'),

    # Cart (DB)
    path('cart/', CartListCreateView.as_view(), name='cart-list'),
    path('cart/<int:id>/', CartDetailView.as_view(), name='cart-detail'),

    # Cart Item (DB)
    path('cart/items/', CartItemCreateView.as_view(), name='cartitem-create'),

    # Session Cart
    path('session/cart/add/', CartSession.as_view(), name='session-cart-add'),
    path('session/cart/', ViewCartAPIView.as_view(), name='session-cart-view'),
]
