from django.shortcuts import render

# Create your views here.
# api/views.py
from rest_framework import generics
from apps.api.models import CtRecord, DRecord, DpuAsKcs, Dpus, RateTableAlls, RateTables
from apps.api.serializers import CtRecordSerializer, DRecordSerializer, DpuAsKcsSerializer, DpusSerializer, RateTableAllsSerializer, RateTablesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CtRecordListCreateView(generics.ListCreateAPIView):
    queryset = CtRecord.objects.all()
    serializer_class = CtRecordSerializer

class DRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DRecordListCreateView(generics.ListCreateAPIView):
    queryset = DRecord.objects.all()
    serializer_class = DRecordSerializer

def drecord_list(request):
    drecords = DRecord.objects.all()
    return render(request, 'common/active_dpu.html', {'drecords': drecords})
    
class DpuAsKcsListCreateView(generics.ListCreateAPIView):
    queryset = DpuAsKcs.objects.all()
    serializer_class = DpuAsKcsSerializer

class DpusListCreateView(generics.ListCreateAPIView):
    queryset = Dpus.objects.all()
    serializer_class = DpusSerializer

class RateTableAllsListCreateView(generics.ListCreateAPIView):
    queryset = RateTableAlls.objects.all()
    serializer_class = RateTableAllsSerializer

class RateTablesListCreateView(generics.ListCreateAPIView):
    queryset = RateTables.objects.all()
    serializer_class = RateTablesSerializer
