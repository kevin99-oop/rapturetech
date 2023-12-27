# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Drec

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
# serializers.py
from rest_framework import serializers
from .models import DPU

class DPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = DPU
        fields = '__all__'




class DrecSerializer(serializers.Serializer):
    REC_TYPE = serializers.CharField(max_length=1)
    SLIP_TYPE = serializers.CharField(max_length=1)
    ST_ID = serializers.CharField(max_length=255)
    CUST_ID = serializers.IntegerField()
    TotalFileRecord = serializers.IntegerField()
    FlagEdited = serializers.CharField(max_length=1)
    MType = serializers.CharField(max_length=1)
    RecordingDate = serializers.DateField()
    SHIFT = serializers.CharField(max_length=1)
    FAT = serializers.FloatField()
    FAT_UNIT = serializers.CharField(max_length=1)
    SNF = serializers.FloatField()
    SNF_UNIT = serializers.CharField(max_length=1)
    CLR = serializers.FloatField()
    CLR_UNIT = serializers.CharField(max_length=1)
    WATER = serializers.FloatField()
    WATER_UNIT = serializers.CharField(max_length=1)
    QT = serializers.FloatField()
    QT_UNIT = serializers.CharField(max_length=1)
    RATE = serializers.FloatField()
    Amount = serializers.FloatField()
    CAmount = serializers.FloatField()
    CSR_NO = serializers.IntegerField()
    CREV = serializers.IntegerField()
    END_TAG = serializers.CharField(max_length=1)
    dpuid = serializers.CharField(max_length=255)

class DrecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drec
        fields = '__all__'

    def create(self, validated_data):
        return Drec.objects.create(**validated_data)