# user/serializers.py

from rest_framework import serializers
from .models import (
    Profile, TwoFactorAuth, CustomUser,
    Address, PaymentMethod
)


# Address
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


# Payment Method
class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


# Profile
class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    payment_method = PaymentMethodSerializer()

    class Meta:
        model = Profile
        fields = [
            'phone', 'bio', 'profile_image',
            'location', 'skills', 'address', 'payment_method'
        ]

    def create(self, validated_data):
        address_data = validated_data.pop('address') #1st Level

        payment_data = validated_data.pop('payment_method') #2nd Level
        address = Address.objects.create(**address_data)
        payment_method = PaymentMethod.objects.create(**payment_data)
        
        return Profile.objects.create(
            address=address,
            payment_method=payment_method,
            **validated_data
        )


# Two Factor Auth
class TwoFactorAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuth
        fields = ['is_enabled']


# User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    two_fa = TwoFactorAuthSerializer(source='twofactorauth', required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'profile', 'two_fa']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        twofa_data = validated_data.pop('twofactorauth', {})
        password = validated_data.pop('password')

        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        profile_serializer = ProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save(user=user)

        if twofa_data:
            TwoFactorAuth.objects.create(user=user, **twofa_data)

        return user
















# from rest_framework import serializers
# from .models import Profile, TwoFactorAuth, CustomUser


# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['phone', 'bio', 'profile_image']

# class TwoFactorAuthSerializer(serializers.ModelSerializer):  # fixed name
#     class Meta:
#         model = TwoFactorAuth
#         fields = ['is_enabled']

# class CustomUserSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer()
#     two_fa = TwoFactorAuthSerializer(source='twofactorauth', required=False)

#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password', 'full_name', 'profile', 'two_fa']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         profile_data = validated_data.pop('profile')
#         twofa_data = validated_data.pop('twofactorauth', {})
#         password = validated_data.pop('password')

#         user = CustomUser.objects.create(**validated_data)
#         user.set_password(password)
#         user.save()

#         Profile.objects.create(user=user, **profile_data)
#         if twofa_data:
#             TwoFactorAuth.objects.create(user=user, **twofa_data)

#         return user