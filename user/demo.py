# models.py
# -------
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Users must have an email address")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     username = None

#     def __str__(self):
#         return self.email

# class Skill(models.Model):
#     name = models.CharField(max_length=40)

#     def str(self):
#         return self.name
# # class Address(models.Model):
# #     street = models.CharField(max_length=150)
# #     city = models.CharField(max_length=100)
# #     state = models.CharField(max_length=100)
# #     zipcode = models.CharField(max_length=20)
# #     country = models.CharField(max_length=100)

# #     def str(self):
# #         return f"{self.street}, {self.city}"
    
# # class PaymentMethod(models.Model):
# #     method_name = models.CharField(max_length=100)
# #     card_number = models.CharField(max_length=20, blank=True, null=True)
# #     expiry_date = models.DateField(blank=True, null=True)
# #     cvv = models.CharField(max_length=4, blank=True, null=True)
# #     billing_address = models.CharField(max_length=50, blank=True, null=True)
    
    
# #     def str(self):
# #         return self.method_name




# class Address(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     street = models.CharField(max_length=100)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     country = models.CharField(max_length=50)
#     zipcode = models.CharField(max_length=20)

# class PaymentMethod(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     method_name = models.CharField(max_length=100)
#     card_number = models.CharField(max_length=16)
#     expiry_date = models.DateField()
#     cvv = models.CharField(max_length=4)
#     billing_address = models.CharField(max_length=100)

    
# class Profile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
#     bio = models.TextField(blank=True)
#     location = models.CharField(max_length=100, blank=True)
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

#     skills = models.ManyToManyField(Skill, blank=True)
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)

#     def str(self):
#         return f"{self.user.full_name}'s Profile"

# serializer.py
# -----------
# from rest_framework import serializers
# from django.contrib.auth import authenticate
# from django.contrib.auth.hashers import make_password
# from .models import (
#     CustomUser,
#     Address,
#     PaymentMethod,
#     Skill,
#     Profile
# )


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         exclude = ['id']

# class PaymentMethodSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentMethod
#         fields = ['method_name', 'card_number', 'expiry_date', 'cvv', 'billing_address']
        

# class ProfileSerializer(serializers.ModelSerializer):
#     skills = serializers.SlugRelatedField(
#         many=True,
#         slug_field='name',
#         queryset=Skill.objects.all()
#     )
#     payment_method = PaymentMethodSerializer()
#     address = AddressSerializer()
    
#     class Meta:
#         model = Profile
#         fields = ['bio', 'location', 'skills', 'payment_method', 'address']

#     def to_representation(self, instance):
#         """Ensure skills are returned as list of names during GET requests."""
#         rep = super().to_representation(instance)
#         rep['skills'] = [skill.name for skill in instance.skills.all()]
#         return rep

# class CustomUserSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer()
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['full_name', 'email', 'password', 'profile']

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         payment_method_data = profile_data.pop('payment_method')
#         address_data = profile_data.pop('address')
#         skills_data = profile_data.pop('skills', [])  

#         user = CustomUser.objects.create(
#             full_name=validated_data.get('full_name'),
#             email=validated_data.get('email'),
#             password=make_password(validated_data['password']),
#         )

#         payment_method = PaymentMethod.objects.create(**payment_method_data)
#         address = Address.objects.create(**address_data)

#         profile = Profile.objects.create(
#             user=user,
#             payment_method=payment_method,
#             address=address,
#             bio=profile_data.get('bio', ''),
#             location=profile_data.get('location', '')
#         )

#         #Add skills after profile is created
#         for skill_name in skills_data:
#             skill_obj, _ = Skill.objects.get_or_create(name=skill_name)
#             profile.skills.add(skill_obj)

#         return user

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         request = self.context.get('request')

#         # Remove unwanted fields in response
#         representation.pop('id', None)
#         representation.pop('username', None)
#         return representation
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(email=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         if not user.is_active:
#             raise serializers.ValidationError("Account disabled")
#         return {'user': user}
    


# # class SkillSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Skill
# #         fields = ['name', 'level']

# urls.py
# --------
# from django.urls import path
# from .views import (
#     SignUpAPIView,
#     MyProfileView,
#     UserProfileDetail,
#     LoginView,
#     LogoutView,
# )

# urlpatterns = [
#     path('signup/', SignUpAPIView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('profile/', MyProfileView.as_view(), name='my-profile'),
#     path('profile/<int:pk>/', UserProfileDetail.as_view(), name='user-profile-detail'),
# ]

# views.py
# ----------
# from django.shortcuts import render
# from rest_framework import generics
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from rest_framework_simplejwt.tokens import RefreshToken
# from apps.custome_serializer.models import CustomUser, Skill
# from apps.custome_serializer.serializers import CustomUserSerializer, LoginSerializer, ProfileSerializer
# from rest_framework.permissions import AllowAny


# class SignUpAPIView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             response_data = {
#             'message': 'User created successfully',
#             'user': CustomUserSerializer(user, context={'request': request}).data
#             }
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class MyProfileView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         user = request.user
#         serializer = CustomUserSerializer(user, context={'request': request})
#         return Response(serializer.data)

#     def put(self, request):
#         user = request.user
#         serializer = CustomUserSerializer(user, data=request.data, partial=True, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class UserProfileDetail(generics.RetrieveAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     lookup_field = 'pk'  
#     permission_classes = []
    
# class LoginView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         })

# class LogoutView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def post(self, request):
#         try:
#             return Response({"message": "Successfully logged out!"}, status=200)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)
            
# admin.py
# --------
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, Profile, Address, PaymentMethod, Skill

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'full_name', 'is_staff', 'is_active')
#     list_filter = ('is_staff', 'is_active')
#     search_fields = ('email',)
#     ordering = ('email',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal Info', {'fields': ('full_name',)}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Profile)
# admin.site.register(Address)
# admin.site.register(PaymentMethod)
# admin.site.register(Skill)

# setting.py
# ..........
# from pathlib import Path

# # Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent


# # Quick-start development settings - unsuitable for production
# # See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# # SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-ch8445-_k*x*fkzfkizak+y(#f$cvq5%jokw)kx)3(&t3&q!@d'

# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

# ALLOWED_HOSTS = []


# # Application definition

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'apps.custome_serializer',
    
# ]

# from datetime import timedelta

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'AUTH_HEADER_TYPES': ('Bearer',),
# }

# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'project.urls'

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'project.wsgi.application'


# # Database
# # https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# # Password validation
# # https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]


# # Internationalization
# # https://docs.djangoproject.com/en/5.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True


# # Static files (CSS, JavaScript, Images)
# # https://docs.djangoproject.com/en/5.2/howto/static-files/

# STATIC_URL = 'static/'

# # Default primary key field type
# # https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# # Custom user model setting
# AUTH_USER_MODEL = 'custome_serializer.CustomUser'


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': [
#         # 'rest_framework.authentication.SessionAuthentication',
#         # 'rest_framework.authentication.BasicAuthentication',
#         # Or use token authentication:
#         # 'rest_framework.authentication.TokenAuthentication',
#          'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ],
#     # 'DEFAULT_PERMISSION_CLASSES': [
#     #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
#     # ]
# }


# project/urls.py
# ----------
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('apps.custome_serializer.urls')),
# ]



# {
#   "email": "{{$randomEmail}}",
#   "full_name": "admin",
#   "password": "Test123!",
#   "profile": {
#     "bio": "I love coding",
#     "location": "Dhaka",
#     "phone": "0123456789",
#     "skills": ["python","django","php"],
#     "payment_method": {
#       "method_name": "MasterCard",
#       "card_number": "4242424242424242",
#       "expiry_date": "2020-06-12",
#       "cvv": "123",
#       "billing_address": "123 Main St"
#     },
#     "address": {
#       "city": "Dhaka",
#       "country": "Bangladesh",
#       "zipcode": "7867",
#       "state": "Dhaka",
#       "street":"hggjh"
#     }
#   }
# }
