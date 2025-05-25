from django.db import models

# Create your models here.
from datetime import datetime
from django.db import models
from django.contrib.auth.hashers import make_password,check_password
# Create your models here.

class mainuser(models.Model):
    user_id=models.AutoField(primary_key=True)
    username = models.CharField(max_length=35, null=False)
    user_mail = models.EmailField(unique=True, null=False)
    user_password = models.CharField(max_length=128, null=False)
    user_dob = models.DateField( null=False)
    user_gender=models.CharField(null=False, max_length=10)
    user_phonenumber = models.BigIntegerField( null=False)
    is_active = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)


    def check_password(self, raw_email,raw_password):
        # Implement password validation logic here
        if (self.user_mail == raw_email) and (self.user_password == raw_password):
            return True
        else:
            return False

    def check_mail(self, mail):
        if self.user_mail == mail:
            return True
        else:
            return False
    
    
    class Meta:
        db_table ="gnanow_mainuser"
        



from django.db import models
from cloudinary.models import CloudinaryField

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = CloudinaryField('image', blank=True, null=True)  # ➕ Add this line

    def __str__(self):
        return self.name

# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Variant Model (color, size, stock)
class ProductVariant(models.Model):
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        # Add more as needed
    ]

    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.CharField(max_length=30, choices=COLOR_CHOICES)
    size = models.CharField(max_length=5, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'color', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"

# Product Images
class ProductImage(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image')  # This stores image on Cloudinary

    def __str__(self):
        return f"Image for {self.variant}"



from django.db import models
from django.utils import timezone
from .models import Product  # assuming it's in the same app

class ProductOffer(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='offer')
    discount_percent = models.PositiveIntegerField(help_text="Enter discount percentage (e.g., 20 for 20%)")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def discounted_price(self):
        if self.is_active():
            return self.product.base_price * (1 - self.discount_percent / 100)
        return self.product.base_price

    def __str__(self):
        return f"{self.product.name} Offer - {self.discount_percent}%"

    class Meta:
        ordering = ['-start_date']



from django.db import models
from django.contrib.auth.models import User

class Wishlist(models.Model):
    user = models.ForeignKey(mainuser, on_delete=models.CASCADE)
    variant = models.ForeignKey('ProductVariant', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'variant')

    def __str__(self):
        return f"{self.user.username} - {self.variant}"



from django.db import models
from django.conf import settings

class CartItem(models.Model):
    user = models.ForeignKey(mainuser, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'variant')  # Prevent duplicates



from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    user = models.ForeignKey(mainuser, on_delete=models.CASCADE, related_name='addresses')
    
    # Address fields
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)  # optional
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    
    # Optional phone number for this address (if needed)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Mark one address as default per user (optional)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.state}, {self.country} - {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Addresses"
        ordering = ['-is_default', '-updated_at']




from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(mainuser, on_delete=models.CASCADE)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    variant = models.ForeignKey('ProductVariant', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price at time of order

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Razorpay', 'Razorpay'),
        ('COD', 'Cash on Delivery'),
        ('Stripe', 'Stripe'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    p_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(mainuser, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} - {self.status} - {self.amount}"






class ProductReview(models.Model):
    productreview_id=models.AutoField(primary_key=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('mainuser', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # ✅ For admin approval

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating}⭐)"



import random
from django.core.mail import send_mail
from django.db import models

class CancelOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
