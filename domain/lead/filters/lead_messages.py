from django_filters import rest_framework as filters
from domain.lead.models import Lead

class LeadMessagesFilter(filters.FilterSet):

    # Lead Model
    first_name = filters.CharFilter(lookup_expr='icontains')
    last_name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    phone_number = filters.CharFilter(lookup_expr='icontains')
    company__name = filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    status__status = filters.CharFilter(field_name='status__status', lookup_expr='exact')
    next_action__action = filters.CharFilter(field_name='next_action__action', lookup_expr='exact')
