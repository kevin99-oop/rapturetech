# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.common.models import DREC

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)

        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class DRECSerializer(serializers.ModelSerializer):
    dpu_id = serializers.CharField(write_only=True)

    class Meta:
        model = DREC
        fields = '__all__'

    def create(self, validated_data):
        dpu_id = validated_data.pop('dpu_id')
        # Assuming you have a method to retrieve or create DPU based on dpu_id
        dpuid_instance = get_or_create_dpu(dpu_id)
        validated_data['dpuid'] = dpuid_instance
        return super().create(validated_data)
    class Meta:
        model = DREC
        fields = '__all__' 
    CLR = serializers.FloatField(required=False)
    WATER = serializers.FloatField(required=False)
    RATE = serializers.FloatField(required=False)
    Amount = serializers.FloatField(required=False)
    CAmount = serializers.FloatField(required=False)
