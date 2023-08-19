from rest_framework import serializers
from . import models
from datetime import datetime

class EventSerializers(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)
    request_user = serializers.SerializerMethodField(read_only=True)
    judul = serializers.CharField(read_only=True,source='title')
    status = serializers.CharField(read_only=True)
    title = serializers.CharField(write_only=True)
    description = serializers.CharField(required=False)
    date = serializers.DateField(write_only=True)
    ticket_quantity = serializers.IntegerField(write_only=True)
    url_detail = serializers.HyperlinkedIdentityField(view_name='event_retreive',lookup_field='id')
    class Meta:
        model = models.Event
        fields = [
            'id',
            'judul',
            'title',
            'date',
            'description',
            'owner',
            'status',
            'request_user',
            'url_detail',
            'ticket_quantity',
            'image'
        ]
    def validate_date(self,value):
        print(value,'va;')
        print(datetime.now().date())
        if value < datetime.now().date():
            raise serializers.ValidationError('tanggal sudah lewat')
        return value
    def get_owner(self,obj):
        return obj.organizer.username

    def get_request_user(self,obj):
        return str(self.context['request'].user)
    