from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8
    )

    class Meta:
        model = User
        fields = ['email', 'useranme', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "Password does not match"}
            )
        
        validate_password(password)

        return attrs
    
    def create(self, validated_data):
        password = validate_password.pop("password")
        validated_data.pop("confirm_password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_password(self, validated_data):
        pass
