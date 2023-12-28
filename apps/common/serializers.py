# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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

# common/serializers.py

from rest_framework import serializers
from apps.common.models import DPU, DREC

class DPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPU
        fields = '__all__'

# serializers.py

from rest_framework import serializers
from apps.common.models import DREC

class DRECCreateSerializer(serializers.ModelSerializer):
    # ... other fields ...

    class Meta:
        model = DREC
        fields = '__all__'
        extra_kwargs = {
            'st_id': {'required': False},
            'recording_date': {'required': False},
            'shift': {'required': False},
            'fat': {'required': False},
            'fat_unit': {'required': False},
            'snf': {'required': False},
            'snf_unit': {'required': False},
            'clr': {'required': False},
            'clr_unit': {'required': False},
            'water': {'required': False},
            'water_unit': {'required': False},
            'qt': {'required': False},
            'qt_unit': {'required': False},
            'rate': {'required': False},
            'amount': {'required': False},
            'camount': {'required': False},
            'csr_no': {'required': False},
            'crev': {'required': False},
            'end_tag': {'required': False},
            'data': {'required': False},
            'dpu': {'required': False},
        }