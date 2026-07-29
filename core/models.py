from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    CATEGORY_CHOICES = (
        ('Burger', 'Burger'),
        ('Sandwich', 'Sandwich'),
        ('Drink', 'Cold Drink'),
        ('Combo', 'Combo Meal'),
    )
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('Placed', 'Order Placed'),
        ('Preparing', 'Preparing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Placed')
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

class DeliveryLocation(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='live_location')
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order.id} Location"