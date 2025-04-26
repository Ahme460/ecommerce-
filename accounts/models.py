from django.db import models
from django.contrib.auth.models import AbstractBaseUser ,BaseUserManager  ,PermissionsMixin

class BaseModel(models.Model):
    """
    This is a abstract model to provide a common base for all
    project models.two datetime fields
    for creation and update date and time.
    """
    created_at = models.DateTimeField(
        verbose_name="Creation Date & Time",
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name="Update Date & Time",
        auto_now=True
    )
    class Meta:
        abstract=True




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        # This method will now return a user based on the provided email.
        return self.get(email=email)


class User(AbstractBaseUser , PermissionsMixin, BaseModel):
    
    name=models.CharField(max_length=500)
    email = models.EmailField(unique=True)
    phone=models.CharField(max_length=50)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super().save(*args, **kwargs)
        
        
    objects = CustomUserManager()
        
    def __str__(self):
        return self.email