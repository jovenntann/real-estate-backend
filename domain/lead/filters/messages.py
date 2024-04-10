from django_filters import rest_framework as filters
from domain.lead.models import Message

class MessageFilter(filters.FilterSet):

    # Message Model
    page__page_name = filters.CharFilter(field_name='page__page_name', lookup_expr='icontains')
    lead__first_name = filters.CharFilter(field_name='lead__first_name', lookup_expr='icontains')
    lead__last_name = filters.CharFilter(field_name='lead__last_name', lookup_expr='icontains')
    source = filters.CharFilter(lookup_expr='icontains')
    sender = filters.CharFilter(lookup_expr='icontains')
    messenger_id = filters.CharFilter(lookup_expr='icontains')
    message = filters.CharFilter(lookup_expr='icontains')
