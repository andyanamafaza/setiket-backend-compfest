from rest_framework import serializers
from . import models
from datetime import datetime
from drf_spectacular.utils import extend_schema_field,OpenApiTypes

class CustomerListEventSerializers(serializers.ModelSerializer):
    organizer = serializers.SerializerMethodField(read_only=True)
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_retreive',lookup_field='id')
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = models.Event
        fields = [
            'id',
            'title',
            'image_url',
            'start_date',
            'city',
            'category',
            'organizer',
            'url_detail',
        ]
    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self,obj):
        return obj.image_url
    @extend_schema_field(OpenApiTypes.STR)
    def get_organizer(self,obj):
        return obj.organizer.username
    
class CustomerDetailEventSerializers(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    organizer = serializers.SerializerMethodField(read_only=True)
    ticket_type = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Event
        fields = [
            'title',
            'image_url',
            'description',
            'start_date',
            'end_date',
            'place_name',
            'city',
            'full_address',
            'location',
            'category',
            'organizer',
            'ticket_type'
        ]
    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self,obj):
        return obj.image_url
    @extend_schema_field(OpenApiTypes.STR)
    def get_organizer(self,obj):
        return obj.organizer.username
    @extend_schema_field(OpenApiTypes.OBJECT)
    def get_ticket_type(self,obj):
        ticket = models.Ticket.objects.filter(event=obj).all()
        if not ticket:
            return []
        return [t.ticket_info() for t in ticket]


class DetailEventSerializers(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
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
            'place_name',
            'city',
            'full_address',
            'location',
            'category',
            'status',
            'is_verified',
            'message',
            'owner',
            'image_url'
        ]
    @extend_schema_field(OpenApiTypes.STR)
    def get_owner(self,obj):
        return obj.organizer.username


class DetailTicketSerializers(serializers.ModelSerializer):
    event_id = serializers.UUIDField()
    id = serializers.CharField(read_only=True)
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
    @extend_schema_field(OpenApiTypes.UUID)
    def create(self, validated_data):
        event_id = validated_data.pop('event_id')
        event = models.Event.objects.get(id=event_id)
        if event:
            if self.context['request'].user == event.organizer:
                price = validated_data.get('price')
                ticket_type = validated_data.get('ticket_type')
                if price >= 0:
                    raise serializers.ValidationError('Price must be greater or equal than 0')
                if price > 0 and ticket_type == 'free':
                    raise serializers.ValidationError('Price must be 0 if ticket type is free')            
                ticket = models.Ticket.objects.create(event=event, **validated_data)
                return ticket
            raise serializers.ValidationError('You are not the owner of this event')
        raise serializers.ValidationError('Event not found')
    

class UserSerializers(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
    image_url = serializers.SerializerMethodField()
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
            'password':{'write_only':True}
        }
    @extend_schema_field(OpenApiTypes.URI)
    def get_image_url(self,obj):
        return obj.image_url
    
    def create(self,validated_data):
        user = models.User.objects.create_user(**validated_data)
        return user
    
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
    owner = serializers.SerializerMethodField(read_only=True)
    banner_url = serializers.CharField(read_only=True)
    proposal_url = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
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
            'is_verified',
            'message',
            'owner',
            'url_detail',
            'banner_url',
            'proposal_url'
        ]
    @extend_schema_field(OpenApiTypes.STR)
    def get_owner(self,obj):
        return obj.organizer.username


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
