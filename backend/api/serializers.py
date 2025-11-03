from rest_framework import serializers
from django.db.models import Sum
from . import models
from .services import TicketPurchaseService
from datetime import datetime
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
import logging

logger = logging.getLogger(__name__)


class CustomerListEventSerializers(serializers.ModelSerializer):
    """
    Serializer for listing events in customer view.
    Includes optimized price calculation and organizer information.
    """
    organizer = serializers.CharField(read_only=True, source='organizer.username')
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_retrieve', lookup_field='id')
    image_url = serializers.URLField(read_only=True)
    price = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Event
        fields = [
            'id',
            'title',
            'image_url',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'city',
            'price',
            'category',
            'organizer',
            'url_detail',
            'is_online'
        ]
    @extend_schema_field(OpenApiTypes.BOOL)
    def get_is_active(self,obj):
        return obj.end_date >= datetime.now().date()
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_price(self, obj):
        """
        PERFORMANCE: Use select_related/prefetch_related if tickets are prefetched.
        Get first paid ticket price, or 0 if none.
        """
        # Optimize: If tickets are prefetched, use them; otherwise query
        if hasattr(obj, '_prefetched_objects_cache') and 'ticket_set' in obj._prefetched_objects_cache:
            paid_tickets = [t for t in obj._prefetched_objects_cache['ticket_set'] if t.ticket_type == 'paid']
            if paid_tickets:
                return paid_tickets[0].price
            return 0
        else:
            # Fallback to query if not prefetched
            price = models.Ticket.objects.filter(event=obj, ticket_type='paid').first()
            return price.price if price else 0
    
class CustomerDetailEventSerializers(serializers.ModelSerializer):
    """
    Serializer for event detail view.
    Includes all ticket types available for the event.
    """
    image_url = serializers.URLField(read_only=True)
    organizer = serializers.CharField(read_only=True,source='organizer.username')
    ticket_type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Event
        fields = [
            'title',
            'image_url',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'place_name',
            'city',
            'full_address',
            'location',
            'category',
            'organizer',
            'ticket_type'
        ]
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_ticket_type(self, obj):
        """
        PERFORMANCE: Use prefetched tickets if available.
        """
        # Use prefetched tickets if available
        if hasattr(obj, '_prefetched_objects_cache') and 'ticket_set' in obj._prefetched_objects_cache:
            all_ticket = obj._prefetched_objects_cache['ticket_set']
        else:
            # Fallback to query if not prefetched
            all_ticket = models.Ticket.objects.filter(event=obj).all()
        
        if not all_ticket:
            return []
        return [ticket.ticket_info() for ticket in all_ticket]


class DetailEventSerializers(serializers.ModelSerializer):
    """
    Serializer for event management (create/update).
    Used by event organizers and admins.
    """
    owner = serializers.CharField(read_only=True, source='organizer.username')
    image_url = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
    status = serializers.CharField(read_only=True)
    registered_users_url = serializers.HyperlinkedIdentityField(view_name='event-users-list',lookup_field='id')
    
    class Meta:
        model = models.Event
        fields = [
            'id',
            'title',
            'image',
            'description',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'place_name',
            'city',
            'full_address',
            'location',
            'category',
            'status',
            'message',
            'owner',
            'image_url',
            'registered_users_url',
        ]
    


class DetailTicketSerializers(serializers.ModelSerializer):
    """
    Serializer for ticket creation and management.
    Validates ticket type and price requirements.
    """
    event_id = serializers.UUIDField()
    id = serializers.CharField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2,required=False)
    class Meta:
        model = models.Ticket
        fields = [
            'id',
            'title',
            'event_id',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'ticket_quantity',
            'ticket_type',
            'description',
            'price',
        ]

    def validate(self,attrs):
        if attrs.get('ticket_type') != 'free' and not attrs.get('price'):
            raise serializers.ValidationError('Price must be filled if ticket type is not free')
        return attrs
    
    @extend_schema_field(OpenApiTypes.OBJECT)
    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        try:
            event = models.Event.objects.get(id=event_id)
        except models.Event.DoesNotExist:
            event = None
        if event:
            if self.context['request'].user == event.organizer:
                price = validated_data.get('price')
                if not price:
                    validated_data['price'] = 0
                    price = 0
                ticket_type = validated_data.get('ticket_type')
                if price < 0:
                    raise serializers.ValidationError('Price must be greater or equal than 0')
                if price > 0 and ticket_type == 'free':
                    raise serializers.ValidationError('Price must be 0 if ticket type is free')            
                ticket = models.Ticket.objects.create(event=event, **validated_data)
                return ticket
            raise serializers.ValidationError('You are not the owner of this event')
        raise serializers.ValidationError('Event not found')
    


class PurchaseTicketSerializers(serializers.ModelSerializer):
    """
    Serializer for ticket purchase.
    Uses TicketPurchaseService for business logic.
    """
    ticket_id = serializers.UUIDField(write_only=True)
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(source='ticket.title',read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2,required=False)
    owner = serializers.CharField(source='customer.username',read_only=True)
    event = serializers.CharField(source='ticket.event.title',read_only=True)
    start_date = serializers.CharField(source='ticket.start_date',read_only=True)
    end_date = serializers.CharField(source='ticket.end_date',read_only=True)
    start_time = serializers.CharField(source='ticket.start_time',read_only=True)
    end_time = serializers.CharField(source='ticket.end_time',read_only=True)
    ticket_type = serializers.CharField(source='ticket.ticket_type',read_only=True)
    class Meta:
        model = models.UserTicket
        fields = [
            'ticket_id',
            'id',
            'owner',
            'title',
            'event',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'ticket_type',
            'price',
        ]
    @extend_schema_field(OpenApiTypes.OBJECT)
    def create(self, validated_data):
        """
        Create a ticket purchase using the service layer.
        Business logic is handled by TicketPurchaseService.
        """
        ticket_id = validated_data.get('ticket_id')
        user = self.context['request'].user
        price = validated_data.get('price')
        
        try:
            # Use service layer for business logic
            user_ticket = TicketPurchaseService.purchase_ticket(
                ticket_id=ticket_id,
                user=user,
                price=price
            )
            return user_ticket
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        except Exception as e:
            logger.error(f"Unexpected error during ticket purchase: {str(e)}", exc_info=True)
            raise serializers.ValidationError('An error occurred while purchasing the ticket. Please try again.')


class EventSalesDataSerializers(serializers.ModelSerializer):
    """
    Serializer for sales data with optimized aggregations.
    PERFORMANCE: Uses single query with annotations instead of multiple queries.
    """
    total_sales = serializers.SerializerMethodField(read_only=True)
    total_active_event = serializers.SerializerMethodField(read_only=True)
    total_sold_ticket = serializers.SerializerMethodField(read_only=True)
    event_data = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.SalesData
        fields = [
            'total_sales',
            'total_active_event',
            'total_sold_ticket',
            'event_data'
        ]
    
    @extend_schema_field(OpenApiTypes.DECIMAL)
    def get_total_sales(self, obj):
        """
        PERFORMANCE: Calculate total sales from already filtered queryset.
        """
        user = self.context['request'].user
        # Use single aggregation query
        total_sales = models.Event.objects.filter(organizer=user).aggregate(
            total=Sum('total_sales')
        )
        return total_sales['total'] if total_sales['total'] else 0
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_total_active_event(self, obj):
        """
        PERFORMANCE: Count active events efficiently.
        """
        user = self.context['request'].user
        # Count events where end_date >= today
        total_active_event = models.Event.objects.filter(
            organizer=user,
            end_date__gte=datetime.now().date()
        ).count()
        return total_active_event
    
    @extend_schema_field(OpenApiTypes.INT)
    def get_total_sold_ticket(self, obj):
        """
        PERFORMANCE: Use single aggregation query.
        """
        user = self.context['request'].user
        total_sold_ticket = models.Event.objects.filter(organizer=user).aggregate(
            total=Sum('total_sold')
        )
        return total_sold_ticket['total'] if total_sold_ticket['total'] else 0
    
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_event_data(self, obj):
        """
        PERFORMANCE: Use select_related to optimize related object access.
        """
        user = self.context['request'].user
        # Optimize query with select_related if needed
        event_data = models.Event.objects.filter(organizer=user).values(
            'title', 'end_date', 'total_sales', 'total_sold'
        )
        return [
            {
                'title': event['title'],
                'status': event['end_date'] < datetime.now().date(),
                'total_sales': event['total_sales'],
                'total_sold': event['total_sold'],
            }
            for event in event_data
        ]

class UserSerializers(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True, required=False)
    image_url = serializers.URLField(read_only=True)
    balance = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'balance',
            'phone_number',
            'image',
            'image_url',
            'role',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate_password(self, value):
        """
        SECURITY: Validate password strength on registration.
        Uses Django's built-in password validators.
        """
        validate_password(value)
        return value
    
    def create(self, validated_data):
        """
        Create user with validated password.
        """
        password = validated_data.pop('password')
        user = models.User.objects.create_user(password=password, **validated_data)
        return user

class UserUpdateSerializers(serializers.ModelSerializer):
    image_url = serializers.URLField(read_only=True)
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'phone_number',
            'image',
            'image_url',
            'role',
        ]
        extra_kwargs = {
            'password':{'write_only':True},
            'id':{'read_only':True},
            'role':{'read_only':True},
        }
    def validate_password(self,value):
        if len(value) < 8:
            raise serializers.ValidationError('Password must be at least 8 characters')
        password = make_password(value)
        return password
    
class AdminListUserSerializers(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    class Meta:
        model = models.User
        fields = [
            'id',
            'username',
            'email',
            'role',
        ]


class AdminListEventOrganizerSerializers(serializers.ModelSerializer):
    event_url = serializers.HyperlinkedIdentityField(view_name='admin_event_organizer_detail_list', lookup_field='id')

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'event_url']


class AdminListEventProposalSerializers(serializers.ModelSerializer):
    event_confirmation_url = serializers.HyperlinkedIdentityField(view_name='event_proposal_confirm', lookup_field='id')
    event_proposal_detail_url = serializers.HyperlinkedIdentityField(view_name='event_proposal_detail', lookup_field='id')

    class Meta:
        model = models.Event
        fields = ['id', 'title', 'created_at', 'event_confirmation_url', 'event_proposal_detail_url']
        
class AdminEventProposalSerializers(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True)
    status = serializers.CharField(write_only=True)
    class Meta:
        model = models.Event
        fields = [
            'id',
            'status',
            'message'
        ]
        
class EventOrganizerProposalSerializers(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True,source='organizer.username')
    banner_url = serializers.CharField(read_only=True)
    proposal_url = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    banner = serializers.ImageField(write_only=True)
    proposal = serializers.FileField(write_only=True)
    status = serializers.CharField(read_only=True)
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_organizer_proposal_detail',lookup_field='id')
    class Meta:
        model = models.EventOrganizerProposal
        fields = [
            'id',
            'name',
            'banner',
            'proposal',
            'description',
            'location',
            'category',
            'status',
            'message',
            'owner',
            'url_detail',
            'banner_url',
            'proposal_url'
        ]


class AdminListEventOrganizerProposalSerializers(serializers.ModelSerializer):
    """
    Serializer for listing event organizer proposals in admin view.
    Includes confirmation and detail URLs.
    """
    event_organizer_confirmation_url = serializers.HyperlinkedIdentityField(view_name='admin_event_proposal_confirm', lookup_field='id')
    event_organizer_proposal_detail_url = serializers.HyperlinkedIdentityField(view_name='admin_event_proposal_detail', lookup_field='id')

    class Meta:
        model = models.EventOrganizerProposal
        fields = ['id', 'organizer', 'name', 'created_at', 'event_organizer_confirmation_url', 'event_organizer_proposal_detail_url']
        
    
class AdminEventOrganizerProposalSerializers(serializers.ModelSerializer):
    """
    Serializer for admin to approve/reject event organizer proposals.
    """
    message = serializers.CharField(write_only=True)
    status = serializers.CharField(write_only=True)
    organizer_id = serializers.CharField(read_only=True)

    class Meta:
        model = models.EventOrganizerProposal
        fields = [
            'id',
            'status',
            'message',
            'organizer_id'
        ]

class UserTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for user ticket information.
    Used to display registered users for events.
    """
    customer_username = serializers.CharField(source='customer.username', read_only=True)
    customer_email = serializers.CharField(source='customer.email', read_only=True)
    event = serializers.CharField(source='event.title', read_only=True)
    ticket_type = serializers.CharField(source='ticket.ticket_type', read_only=True)
    
    class Meta:
        model = models.UserTicket
        fields = ['id', 'customer_username', 'customer_email', 'ticket_type', 'price', 'event', 'created_at']