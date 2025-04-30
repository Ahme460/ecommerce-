from django.db import models
from accounts.models import User, BaseModel
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Category(BaseModel):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name

class Product(BaseModel):
    STATUS_CHOICES = (
        ('sold', 'Sold'),
        ('sold_out', 'Sold Out'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category_product')

    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"

class Box(BaseModel):
    category= models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category_box')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='box')

    def __str__(self):
        return self.name

class BoxImage(BaseModel):
    box = models.ForeignKey(Box, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='boxs/')

    def __str__(self):
        return f"Image of {self.box.name}"

class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user.email} - {self.content_object}"


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email}'s Cart"



class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.content_object}"
