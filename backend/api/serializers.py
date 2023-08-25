from rest_framework import serializers
from . import models
from datetime import datetime
from drf_spectacular.utils import extend_schema_field,OpenApiTypes
from django.contrib.auth.hashers import make_password
class CustomerListEventSerializers(serializers.ModelSerializer):
    organizer = serializers.CharField(read_only=True,source='organizer.username')
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_retreive',lookup_field='id')
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
        ]
    @extend_schema_field(OpenApiTypes.INT)
    def get_price(self,obj):
        price = models.Ticket.objects.filter(event=obj,ticket_type='paid').first()
        price = price.price if price else 0
        return price
    
class CustomerDetailEventSerializers(serializers.ModelSerializer):
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
    def get_ticket_type(self,obj):
        all_ticket = models.Ticket.objects.filter(event=obj).all()
        if not all_ticket:
            return []
        return [ticket.ticket_info() for ticket in all_ticket]


class DetailEventSerializers(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True,source='organizer.username')
    image_url = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
    status = serializers.CharField(read_only=True)
    
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
            'image_url'
        ]
    


class DetailTicketSerializers(serializers.ModelSerializer):
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
    def create(self,validated_data):
        try:
            ticket = models.Ticket.objects.get(id=validated_data.get('ticket_id'))
        except models.Ticket.DoesNotExist:
            ticket = None
        if ticket:
            price = ticket.price
            if ticket.ticket_type == 'relawan':
                price = validated_data.get('price') if validated_data.get('price') else 0
                if price < ticket.price:
                    raise serializers.ValidationError('Price must be greater or equal than minimum ticket price')
            if ticket.ticket_quantity > 0:
                self.context['request'].user.balance -= price
                self.context['request'].user.save()
                ticket.ticket_quantity -= 1
                ticket.save()
                print(ticket.event,'ticket eventtt')
                try:
                    sales_data = models.SalesData.objects.get(event=ticket.event)
                except models.SalesData.DoesNotExist:
                    sales_data = None
                if not sales_data:
                    sales_data = models.SalesData.objects.create(
                        event=ticket.event,
                        amount = 0,
                    )
                sales_data.amount += price
                sales_data.save()
                user_ticket = models.UserTicket.objects.create(
                    customer=self.context['request'].user,
                    ticket=ticket,
                    price=price,
                    event=ticket.event,
                    sales_data=sales_data
                    )
                return user_ticket
            raise serializers.ValidationError('Ticket is sold out')
        raise serializers.ValidationError('Ticket not found')


class UserSerializers(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
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
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        user = models.User.objects.create_user(**validated_data)
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


class AdminListEventProposalSerializers(serializers.ModelSerializer):
    event_organizer_confirmation_url = serializers.HyperlinkedIdentityField(view_name='admin_event_proposal_confirm', lookup_field='id')
    event_organizer_proposal_detail_url = serializers.HyperlinkedIdentityField(view_name='admin_event_proposal_detail', lookup_field='id')

    class Meta:
        model = models.EventOrganizerProposal
        fields = ['id', 'organizer', 'name', 'created_at', 'event_organizer_confirmation_url', 'event_organizer_proposal_detail_url']
        
    
class AdminEventProposalSerializers(serializers.ModelSerializer):
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
