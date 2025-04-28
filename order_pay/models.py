from django.db import models
from accounts.models import (
    User,
    BaseModel
)

class Order(BaseModel):

    STATUS_ORDER=(
        ("Payment upon receipt", "Payment upon receipt"),
        ("paid","paid")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100,choices=STATUS_ORDER)   
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"