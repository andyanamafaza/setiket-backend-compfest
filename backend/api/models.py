from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
from datetime import datetime
import uuid
import os

class User(AbstractUser): 
    ROLES = (
        ('customer', 'Customer'),
        ('event_organizer', 'Event Organizer'),
        ('administrator', 'Administrator'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, unique=True, blank=False,default='0812')
    image = CloudinaryField(
        'image',
        resource_type='image',
        )
    role = models.CharField(max_length=15, choices=ROLES, default='customer', blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __repr__(self):
        return f'{self.username}, {self.email}, {self.role}'
    
    def get_image_url(self):
        return'{}{}'.format(settings.CLOUDINARY_ROOT_URL,self.image)

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    CATEGORY_CHOICES = (
        ('seminar', 'Seminar'),
        ('konser', 'Konser'),
        ('horror', 'Horror'),
        ('komedi', 'Komedi'),
        ('olahraga', 'Olahraga'),
    )
    title = models.CharField(max_length=255, blank=False)
    image = CloudinaryField(
        'image',
        resource_type='image'
        )
    
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    place_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_address = models.TextField()
    location = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    is_verified = models.BooleanField(default=True)
    message = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_image_url(self):
        return'{}{}'.format(settings.CLOUDINARY_ROOT_URL,self.image)

class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('free', 'Free'),
        ('relawan', 'Relawan'),
        ('paid', 'Paid'),
    )
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    ticket_quantity = models.IntegerField()
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class UserTicket(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class EventOrganizerProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    banner = CloudinaryField(
        'image',
        resource_type='image'
        )
    proposal = models.FileField(upload_to='proposals/')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class SalesData(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(UserTicket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)