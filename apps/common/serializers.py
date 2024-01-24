# myapp/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.common.models import DREC,Customer,TextFile

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
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class CIDRangeSerializer(serializers.Serializer):
    start_range = serializers.IntegerField()
    end_range = serializers.IntegerField()



class TextFileSerializer(serializers.ModelSerializer):
    file_link = serializers.SerializerMethodField()

    class Meta:
        model = TextFile
        fields = ['user', 'st_id', 'file_link', 'upload_date']

    def get_file_link(self, obj):
        return obj.file.url