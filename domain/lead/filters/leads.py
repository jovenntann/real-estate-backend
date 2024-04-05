from django_filters import rest_framework as filters
from domain.lead.models import Lead

class LeadFilter(filters.FilterSet):

    # Lead Model
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    phone_number = filters.CharFilter(lookup_expr='icontains')
    company__name = filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    status__name = filters.CharFilter(field_name='status__name', lookup_expr='icontains')
