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
    class Meta:
        model = DREC
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        dpuid = instance.dpuid.st_id if instance.dpuid else None  # Assuming dpuid is a ForeignKey to DPU
        return {
            "REC_TYPE": representation["REC_TYPE"],
            "SLIP_TYPE": representation["SLIP_TYPE"],
            "ST_ID": representation["ST_ID"],
            "CUST_ID": representation["CUST_ID"],
            "TotalFileRecord": representation["TotalFileRecord"],
            "FlagEdited": representation["FlagEdited"],
            "MType": representation["MType"],
            "RecordingDate": representation["RecordingDate"],
            "SHIFT": representation["SHIFT"],
            "FAT": representation["FAT"],
            "FAT_UNIT": representation["FAT_UNIT"],
            "SNF": representation["SNF"],
            "SNF_UNIT": representation["SNF_UNIT"],
            "CLR": representation["CLR"],
            "CLR_UNIT": representation["CLR_UNIT"],
            "WATER": representation["WATER"],
            "WATER_UNIT": representation["WATER_UNIT"],
            "QT": representation["QT"],
            "QT_UNIT": representation["QT_UNIT"],
            "RATE": representation["RATE"],
            "Amount": representation["Amount"],
            "CAmount": representation["CAmount"],
            "CSR_NO": representation["CSR_NO"],
            "CREV": representation["CREV"],
            "END_TAG": representation["END_TAG"],
            "dpuid": dpuid,
        }