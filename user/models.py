# user/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


# Address Model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}"


# Payment Method Model
class PaymentMethod(models.Model):
    method_name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=16)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    billing_address = models.TextField()

    def __str__(self):
        return self.method_name


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list, blank=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.OneToOneField(PaymentMethod, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} Profile"


# Activity Log
class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"


# User Session
class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255)
    device = models.CharField(max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    last_active = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Session"


# Two Factor Authentication
class TwoFactorAuth(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=255, blank=True)
    last_verified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - 2FA"















































# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.conf import settings


# # Custom User Manager

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError(_('Email is required'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password) #Hashing password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if not extra_fields.get('is_staff'):
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if not extra_fields.get('is_superuser'):
#             raise ValueError(_('Superuser must have is_superuser=True.'))

#         return self.create_user(email, password, **extra_fields)


# # Custom User Model

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     email_verified = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []  # When you create a user via createsuperuser command, only the email (which is the USERNAME_FIELD) and password are required.

#     def __str__(self):
#         return self.email


# # User Profile

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=20, blank=True)
#     profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
#     bio = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.user.email} Profile"


# # Activity Log

# class ActivityLog(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     action = models.CharField(max_length=255)  # e.g. "Login", "Password Changed"
#     ip_address = models.GenericIPAddressField(blank=True, null=True)
#     user_agent = models.TextField(blank=True, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True) #Automatically sets the timestamp only once when the object is created.

#     def __str__(self):
#         return f"{self.user.email} - {self.action} at {self.timestamp}"
    

# # User Session


# class UserSession(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     session_key = models.CharField(max_length=255)
#     device = models.CharField(max_length=255, blank=True)
#     ip_address = models.GenericIPAddressField(blank=True, null=True)
#     user_agent = models.TextField(blank=True, null=True)
#     last_active = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.email} - Session"


# # Two Factor Authentication

# class TwoFactorAuth(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     is_enabled = models.BooleanField(default=False)
#     secret_key = models.CharField(max_length=255, blank=True)
#     last_verified = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.user.email} - 2FA"