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
    # def get_request_user(self,obj):
    #     return str(self.context['request'].user)
    

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