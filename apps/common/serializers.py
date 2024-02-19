# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from apps.common.models import DREC, Customer, Config,RateTable

# Serializer for User model, includes password validation
class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password1', 'password2')

    def validate(self, data):
        # Validate that the passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Create a new user with the provided data
        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user

# Serializer for user login information
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

# Serializer for DREC model
class DRECSerializer(serializers.ModelSerializer):
    class Meta:
        model = DREC
        fields = '__all__'

# Serializer for Customer model
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Serializer for CIDRange
class CIDRangeSerializer(serializers.Serializer):
    start_range = serializers.IntegerField()
    end_range = serializers.IntegerField()

# Another CustomerSerializer for a specific set of fields
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'st_id', 'csv_file', 'date_uploaded']  # Add 'date_uploaded'

# Serializer for Config model
class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = '__all__'
