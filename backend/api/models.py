from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from .storage import SeaweedFSStorage
import uuid
from datetime import datetime

# Initialize SeaweedFS storage
seaweedfs_storage = SeaweedFSStorage()

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Supports three roles: customer, event_organizer, and administrator.
    Includes balance tracking and profile image support via SeaweedFS.
    """
    ROLES = (
        ('customer', 'Customer'),
        ('event_organizer', 'Event Organizer'),
        ('administrator', 'Administrator'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, blank=False, db_index=True)
    email = models.EmailField(unique=True, blank=False, db_index=True)
    balance = models.IntegerField(default=1000000)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    image = models.ImageField(upload_to='users/', storage=seaweedfs_storage, blank=True, null=True)
    role = models.CharField(max_length=15, choices=ROLES, default='customer', blank=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f'{settings.SEAWEEDFS_URL}/filer/users/default.png'
    def __repr__(self):
        return f'{self.username}, {self.email}, {self.role}'


class Event(models.Model):
    """
    Event model representing an event that can be organized.
    Events require admin approval before being visible to customers.
    Tracks sales and ticket statistics.
    """
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
    image = models.ImageField(upload_to='events/', storage=seaweedfs_storage)
    description = models.TextField()
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    place_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, db_index=True)
    full_address = models.TextField()
    total_sold = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, db_index=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', db_index=True)
    message = models.TextField()
    is_online = models.BooleanField(default=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'end_date']),  # Composite index for common queries
            models.Index(fields=['category', 'status']),  # Composite index for category filtering
            models.Index(fields=['organizer', 'status']),  # Composite index for organizer events
        ]
    
    def clean(self):
        """
        Validate that end_date is after start_date.
        """
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': 'End date must be after start date.'
                })
        if self.start_time and self.end_time and self.start_date == self.end_date:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'End time must be after start time when on the same day.'
                })
    
    def save(self, *args, **kwargs):
        """
        Run validation before saving.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return f'{settings.SEAWEEDFS_URL}/filer/events/default.png'
    def get_short_description(self):
        return {
            'title':self.title,
            'status':self.end_date < datetime.now().date(),
            'total_sales':self.total_sales,
            'total_sold':self.total_sold,
        }

class Ticket(models.Model):
    """
    Ticket model representing a ticket type for an event.
    Supports three types: free, relawan (volunteer/donation), and paid.
    Tracks quantity and sale period.
    """
    TICKET_TYPE_CHOICES = (
        ('free', 'Free'),
        ('relawan', 'Relawan'),
        ('paid', 'Paid'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    ticket_quantity = models.IntegerField()
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE_CHOICES, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['event', 'ticket_type']),  # Composite index for event tickets
        ]
    
    def clean(self):
        """
        Validate that end_date is after start_date.
        """
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError({
                    'end_date': 'End date must be after start date.'
                })
        if self.start_time and self.end_time and self.start_date == self.end_date:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'End time must be after start time when on the same day.'
                })
    
    def save(self, *args, **kwargs):
        """
        Run validation before saving.
        """
        self.full_clean()
        super().save(*args, **kwargs)
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
    """
    UserTicket model representing a ticket purchase by a customer.
    Links customer, ticket, event, and sales data.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    sales_data = models.ForeignKey('SalesData', on_delete=models.CASCADE, null=True)
    qr_code = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['customer', 'event']),  # Composite index for user event queries
        ]

class EventOrganizerProposal(models.Model):
    """
    EventOrganizerProposal model for users to submit proposals to become event organizers.
    Requires admin approval before user role is updated.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    location = models.TextField()
    banner = models.ImageField(upload_to='proposals/banners/', storage=seaweedfs_storage)
    proposal = models.FileField(upload_to='proposals/documents/', storage=seaweedfs_storage)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', db_index=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organizer', 'status'],
                condition=models.Q(status='pending'),
                name='unique_pending_proposal_per_user'
            )
        ]
    @property
    def banner_url(self):
        if self.banner:
            return self.banner.url
        return None
    
    @property
    def proposal_url(self):
        if self.proposal:
            return self.proposal.url
        return None


class SalesData(models.Model):
    """
    SalesData model tracking sales statistics for events.
    One record per event-organizer pair.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, db_index=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = [['event', 'organizer']]  # One sales data per event-organizer pair
