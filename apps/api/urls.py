# myapp/urls.py
from django.urls import path
from .views import (
    CtRecordListCreateView,
    DRecordListCreateView,
    DpuAsKcsListCreateView,
    DpusListCreateView,
    RateTableAllsListCreateView,
    RateTablesListCreateView,
)
from .views import DRecordAPIView,drecord_list


urlpatterns = [
    path('ctrecords/', CtRecordListCreateView.as_view(), name='ctrecord-list-create'),
    path('drec/', DRecordAPIView.as_view(), name='drecord-list-create'),
    path('dpuaskcs/', DpuAsKcsListCreateView.as_view(), name='dpuaskcs-list-create'),
    path('dpus/', DpusListCreateView.as_view(), name='dpus-list-create'),
    path('ratetablealls/', RateTableAllsListCreateView.as_view(), name='ratetablealls-list-create'),
    path('ratetables/', RateTablesListCreateView.as_view(), name='ratetables-list-create'),
    # Add other URL patterns as needed
    path('drec/', drecord_list, name='drecord-list'),

]