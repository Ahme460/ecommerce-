from django.db import models
from accounts.models import User, BaseModel

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image of {self.product.name}"

class Book(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    products = models.ManyToManyField(Product, related_name='books')

    def __str__(self):
        return self.name

class BookImage(BaseModel):
    book = models.ForeignKey(Book, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return f"Image of {self.book.name}"

class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} wishlist - {self.product.name}"
