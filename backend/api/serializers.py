from rest_framework import serializers
from . import models
from datetime import datetime

class EventSerializers(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    image_url = serializers.CharField(read_only=True)
    is_verified = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
    status = serializers.CharField(read_only=True)
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_retreive',lookup_field='id')
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
            'url_detail',
            'image_url'
        ]
    def get_owner(self,obj):
        return obj.organizer.username


class UserSerializers(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)
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
