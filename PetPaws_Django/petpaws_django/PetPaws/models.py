from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# Custom User Manager
class AppUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Custom User Model
class AppUser(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    role = models.CharField(max_length=50, default='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'address', 'gender']

    objects = AppUserManager()

    def __str__(self):
        return self.email


# PET MODEL
class Pet(models.Model):
    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Adopted', 'Adopted'),
        ('Under Review', 'Under Review'),
        ('Sold', 'Sold'),
    ]

    PET_TYPE_CHOICES = [
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Bird', 'Bird'),
        ('Horse', 'Horse'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='pet_images/', default='pet_images/default_pet.jpg')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Available')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pets')
    medical_issues = models.CharField(max_length=255, blank=True, null=True)
    pet_type = models.CharField(max_length=50, choices=PET_TYPE_CHOICES)
    other_pet_type = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'pet')

    def __str__(self):
        return f"{self.user.email} - {self.pet.name}"
    

# class Notification(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
#     message = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ['-created_at']  # Show latest notifications first

#     def __str__(self):
#         return f"To {self.user.email}: {self.message[:30]}"

#     def mark_as_read(self):
#         self.is_read = True
#         self.save()


# class AdoptionRequest(models.Model):
#     pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
#     adopter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_requests')
#     status = models.CharField(max_length=20, choices=[('Under Review', 'Under Review'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Under Review')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('pet', 'adopter')  # prevent same user from sending multiple requests

#     def __str__(self):
#         return f"{self.adopter.name} → {self.pet.name} ({self.status})"
