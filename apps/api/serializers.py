# myapp/serializers.py
from rest_framework import serializers
from .models import CtRecord, DRecord, DpuAsKcs, Dpus, RateTableAlls, RateTables

class CtRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CtRecord
        fields = '__all__'

class DRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRecord
        fields = '__all__'

class DpuAsKcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DpuAsKcs
        fields = '__all__'

class DpusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dpus
        fields = '__all__'

class RateTableAllsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateTableAlls
        fields = '__all__'

class RateTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateTables
        fields = '__all__'
