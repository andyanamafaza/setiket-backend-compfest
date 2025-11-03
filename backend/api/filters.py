"""
Filter sets for API endpoints.
Provides filtering, searching, and sorting capabilities.
"""
import django_filters
from . import models
from django.db import models as django_models


class EventFilter(django_filters.FilterSet):
    """
    Filter set for Event model.
    Supports filtering by category, status, city, date range, and organizer.
    """
    category = django_filters.ChoiceFilter(choices=models.Event.CATEGORY_CHOICES)
    status = django_filters.ChoiceFilter(choices=models.Event.STATUS_CHOICES)
    city = django_filters.CharFilter(lookup_expr='icontains')
    organizer = django_filters.CharFilter(field_name='organizer__username', lookup_expr='icontains')
    is_online = django_filters.BooleanFilter()
    
    # Date range filtering
    start_date_from = django_filters.DateFilter(field_name='start_date', lookup_expr='gte')
    start_date_to = django_filters.DateFilter(field_name='start_date', lookup_expr='lte')
    end_date_from = django_filters.DateFilter(field_name='end_date', lookup_expr='gte')
    end_date_to = django_filters.DateFilter(field_name='end_date', lookup_expr='lte')
    
    # Price range filtering (from tickets)
    min_price = django_filters.NumberFilter(method='filter_min_price')
    max_price = django_filters.NumberFilter(method='filter_max_price')
    
    class Meta:
        model = models.Event
        fields = ['category', 'status', 'city', 'organizer', 'is_online']
    
    def filter_min_price(self, queryset, name, value):
        """Filter events with tickets priced at least value."""
        return queryset.filter(ticket__price__gte=value, ticket__ticket_type='paid').distinct()
    
    def filter_max_price(self, queryset, name, value):
        """Filter events with tickets priced at most value."""
        return queryset.filter(ticket__price__lte=value, ticket__ticket_type='paid').distinct()


class TicketFilter(django_filters.FilterSet):
    """
    Filter set for Ticket model.
    Supports filtering by event, ticket type, and price range.
    """
    event = django_filters.UUIDFilter(field_name='event__id')
    ticket_type = django_filters.ChoiceFilter(choices=models.Ticket.TICKET_TYPE_CHOICES)
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    available = django_filters.BooleanFilter(method='filter_available')
    
    class Meta:
        model = models.Ticket
        fields = ['event', 'ticket_type', 'min_price', 'max_price']
    
    def filter_available(self, queryset, name, value):
        """Filter tickets by availability."""
        if value:
            return queryset.filter(ticket_quantity__gt=0)
        return queryset.filter(ticket_quantity=0)


class UserFilter(django_filters.FilterSet):
    """
    Filter set for User model.
    Supports filtering by role, username, and email.
    """
    role = django_filters.ChoiceFilter(choices=models.User.ROLES)
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = models.User
        fields = ['role', 'username', 'email']


class UserTicketFilter(django_filters.FilterSet):
    """
    Filter set for UserTicket model.
    Supports filtering by customer, event, and ticket type.
    """
    customer = django_filters.UUIDFilter(field_name='customer__id')
    event = django_filters.UUIDFilter(field_name='event__id')
    ticket_type = django_filters.CharFilter(field_name='ticket__ticket_type')
    
    class Meta:
        model = models.UserTicket
        fields = ['customer', 'event', 'ticket_type']


class EventOrganizerProposalFilter(django_filters.FilterSet):
    """
    Filter set for EventOrganizerProposal model.
    Supports filtering by status and organizer.
    """
    status = django_filters.ChoiceFilter(choices=models.EventOrganizerProposal.STATUS_CHOICES)
    organizer = django_filters.UUIDFilter(field_name='organizer__id')
    
    class Meta:
        model = models.EventOrganizerProposal
        fields = ['status', 'organizer']

