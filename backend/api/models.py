from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from cloudinary.models import CloudinaryField
import uuid
from datetime import datetime

class User(AbstractUser):
    ROLES = (
        ('customer', 'Customer'),
        ('event_organizer', 'Event Organizer'),
        ('administrator', 'Administrator'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=False)
    email = models.EmailField(unique=True, blank=False)
    balance = models.IntegerField(default=1000000)
    phone_number = models.CharField(max_length=15, unique=True, blank=True,null=True, default='0812')
    image = CloudinaryField('image', resource_type='image',blank=True,null=True)
    role = models.CharField(max_length=15, choices=ROLES, default='customer', blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    @property
    def image_url(self):
        self.image = self.image if self.image else 'ioacxjfdtuyrilislfgw'
        return '{}{}'.format(settings.CLOUDINARY_ROOT_URL, self.image)
    def __repr__(self):
        return f'{self.username}, {self.email}, {self.role}'


class Event(models.Model):
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
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False)
    image = CloudinaryField('image', resource_type='image')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    place_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    full_address = models.TextField()
    location = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    is_online = models.BooleanField(default=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def image_url(self):
        return '{}{}'.format(settings.CLOUDINARY_ROOT_URL, self.image)


class Ticket(models.Model):
    TICKET_TYPE_CHOICES = (
        ('free', 'Free'),
        ('relawan', 'Relawan'),
        ('paid', 'Paid'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    def ticket_info(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'ticket_quantity': self.ticket_quantity,
            'ticket_type': self.ticket_type,
            'description': self.description,
            'price': self.price,
        }

class UserTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    sales_data = models.ForeignKey('SalesData', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class EventOrganizerProposal(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    banner = CloudinaryField('banner', resource_type='image')
    proposal = CloudinaryField('proposals', resource_type='image')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def banner_url(self):
        return '{}{}'.format(settings.CLOUDINARY_ROOT_URL, self.banner)
    @property
    def proposal_url(self):
        return '{}{}'.format(settings.CLOUDINARY_ROOT_URL, self.proposal)


class SalesData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
