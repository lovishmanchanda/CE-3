from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class CareTip(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Pet Hospital Info
class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    emergency_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Pet Food
class Food(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='petcare_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"


# Pet Clothes
class Clothes(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='clothes_images/', blank=True, null=True)


    def __str__(self):
        return self.name


# Pet Medicines
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    usage = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='petcare_images/', blank=True, null=True)

    def __str__(self):
        return self.name


# Pet Accessories
class Accessory(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='petcare_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    # cart items

class CartItem(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('medicine', 'Medicine'),
        ('accessory', 'Accessory'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_id = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.category} (ID {self.product_id}) x {self.quantity}"