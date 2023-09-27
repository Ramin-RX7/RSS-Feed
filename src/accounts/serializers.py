from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)  # write_only=True is not needed

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        del validated_data['password2']
        return super().create(validated_data)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def save(self):
        instance = super().save()
        instance.set_password(self.validated_data["password"])
        instance.save()
        return instance



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(
        validators = (validate_password,)
    )
    confirm_password = serializers.CharField()

    def validate_new_password(self, value):
        if 128<len(value):
            raise ValidationError("Password must have length between 6-125")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data



class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        validators = (validate_password,)
    )
    confirm_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if 128<len(value):
            raise ValidationError("Password must have length between 6-125")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return data
