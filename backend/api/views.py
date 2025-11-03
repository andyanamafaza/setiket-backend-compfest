from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.conf import settings
from . import models
from . import permissions as custom_permissions
from . import filters
from .serializers import (
    CustomerDetailEventSerializers,
    CustomerListEventSerializers,
    DetailEventSerializers,
    DetailTicketSerializers,
    PurchaseTicketSerializers,
    EventSalesDataSerializers,
    UserSerializers,
    UserUpdateSerializers,
    AdminListUserSerializers,
    AdminListEventOrganizerSerializers,
    AdminListEventProposalSerializers,
    AdminEventProposalSerializers,
    EventOrganizerProposalSerializers,
    AdminListEventOrganizerProposalSerializers,
    AdminEventOrganizerProposalSerializers,
    UserTicketSerializer,
)
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CustomerEventRetrieveView(generics.RetrieveAPIView):
    """
    Public endpoint to retrieve event details.
    SECURITY: No authentication required for public event viewing.
    """
    queryset = models.Event.objects.select_related('organizer').prefetch_related('ticket_set')
    serializer_class = CustomerDetailEventSerializers
    lookup_field = 'id'
    # SECURITY: Use default authentication (JWT only in production)
    authentication_classes = [JWTAuthentication] if not settings.DEBUG else []
    permission_classes = [permissions.AllowAny]


@extend_schema_view(get=extend_schema(
    parameters=[
        OpenApiParameter(name='category', description='Category Name', type=str, required=False),
        OpenApiParameter(name='city', description='City name (partial match)', type=str, required=False),
        OpenApiParameter(name='start_date_from', description='Filter events starting from this date', type=str, required=False),
        OpenApiParameter(name='start_date_to', description='Filter events starting until this date', type=str, required=False),
        OpenApiParameter(name='min_price', description='Minimum ticket price', type=float, required=False),
        OpenApiParameter(name='max_price', description='Maximum ticket price', type=float, required=False),
        OpenApiParameter(name='search', description='Search in title and description', type=str, required=False),
        OpenApiParameter(name='ordering', description='Order by field (e.g., -start_date, city)', type=str, required=False),
    ]
))
class CustomerEventListView(generics.ListAPIView):
    """
    List events with filtering, searching, and sorting capabilities.
    
    Filtering:
    - category: Filter by event category
    - city: Filter by city (partial match)
    - start_date_from/to: Filter by start date range
    - min_price/max_price: Filter by ticket price range
    - search: Search in title and description
    
    Sorting:
    - ordering: Sort by any field (prefix with - for descending)
    - Examples: ordering=start_date, ordering=-created_at, ordering=city
    
    SECURITY: Requires authentication (JWT only in production).
    """
    queryset = models.Event.objects.all()
    serializer_class = CustomerListEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsCustomerOrAdmin]
    filterset_class = filters.EventFilter
    search_fields = ['title', 'description', 'city', 'place_name']
    ordering_fields = ['start_date', 'end_date', 'created_at', 'city', 'title', 'total_sales']
    ordering = ['-created_at']  # Default ordering
    
    def get_queryset(self):
        """
        Get queryset with optimizations and default filters.
        Only shows approved events that haven't ended.
        """
        queryset = self.queryset.select_related('organizer').prefetch_related('ticket_set')
        
        # Apply default filters for customer view
        queryset = queryset.filter(status='approved', end_date__gte=datetime.now().date())
        
        # Backward compatibility: support old category filter
        category = self.request.query_params.get('category')
        if category and 'category' not in self.request.query_params:
            queryset = queryset.filter(category=category)
        
        return queryset
    
class CustomerUpcomingEventListView(generics.ListAPIView):
    """
    List upcoming events for authenticated user.
    SECURITY: Requires authentication (JWT only in production).
    """
    serializer_class = CustomerListEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsCustomerOrAdmin]

    def get_queryset(self):
        # PERFORMANCE: Optimize query with select_related and prefetch_related
        user = self.request.user
        user_tickets = models.UserTicket.objects.filter(customer=user).values_list('event_id', flat=True)
        return models.Event.objects.select_related('organizer').prefetch_related('ticket_set').filter(
            id__in=user_tickets,
            status='approved',
            end_date__gte=datetime.now().date()
        )
class EventCreateView(generics.CreateAPIView):
    """
    Create a new event.
    SECURITY: Requires event organizer or admin role (JWT only in production).
    """
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        description = serializer.validated_data.get('description') or 'this is default for description'
        serializer.save(organizer=self.request.user, description=description)

class TicketCreateView(generics.CreateAPIView):
    """
    Create a new ticket for an event.
    SECURITY: Requires event organizer or admin role (JWT only in production).
    """
    queryset = models.Ticket.objects.all()
    serializer_class = DetailTicketSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

class TicketPurchaseView(generics.CreateAPIView):
    """
    Purchase a ticket.
    SECURITY: Requires authentication. Uses atomic transactions to prevent race conditions.
    """
    queryset = models.UserTicket.objects.all()
    serializer_class = PurchaseTicketSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

class EventUpdateView(generics.UpdateAPIView):
    """
    Update an event.
    SECURITY: Only owner or admin can update (JWT only in production).
    """
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrOwner]
    lookup_field = 'id'

class EventSalesDataView(generics.RetrieveAPIView):
    """
    Retrieve sales data for event organizer.
    SECURITY: Requires event organizer or admin role (JWT only in production).
    """
    queryset = models.SalesData.objects.all()
    serializer_class = EventSalesDataSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user.id).first()
    def get_object(self):
        return self.get_queryset()


class EventListOwnerView(generics.ListAPIView):
    """
    List events owned by the authenticated user.
    SECURITY: Requires authentication (JWT only in production).
    """
    queryset = models.Event.objects.select_related('organizer').prefetch_related('ticket_set')
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailEventSerializers
    
    def get_queryset(self):
        # PERFORMANCE: select_related already applied to queryset
        return self.queryset.filter(organizer=self.request.user)

class RegisterUserView(generics.CreateAPIView):
    """
    Register a new user.
    SECURITY: Public endpoint, validates password strength.
    """
    queryset = models.User.objects.all()
    serializer_class = UserSerializers
    # SECURITY: Public endpoint, no authentication required
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


class LogoutView(generics.GenericAPIView):
    """
    Logout user by blacklisting refresh token.
    SECURITY: Requires authentication, catches specific exceptions.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """
        Blacklist the refresh token.
        """
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response(
                    {'error': 'refresh_token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info(f"User {request.user.username} logged out successfully")
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except TokenError as e:
            logger.warning(f"Invalid token during logout: {str(e)}")
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Logout failed for user {request.user.username}: {str(e)}", exc_info=True)
            return Response(
                {'error': 'Logout failed. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class AdminListUserView(generics.ListAPIView):
    """
    List all users with filtering and sorting.
    
    Filtering:
    - role: Filter by user role
    - username: Filter by username (partial match)
    - email: Filter by email (partial match)
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, username)
    """
    queryset = models.User.objects.all()
    serializer_class = AdminListUserSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    filterset_class = filters.UserFilter
    search_fields = ['username', 'email']
    ordering_fields = ['created_at', 'username', 'email', 'role']
    ordering = ['-created_at']

class AdminEventOrganizerDetailListView(generics.ListAPIView):
    """
    List events by organizer for admin.
    PERFORMANCE: Uses select_related to avoid N+1 queries.
    """
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

    def get_queryset(self):
        # PERFORMANCE: Use select_related to join organizer
        organizer_id = self.kwargs['id']
        return models.Event.objects.select_related('organizer').prefetch_related('ticket_set').filter(organizer_id=organizer_id)

class AdminListEventOrganizerView(generics.ListAPIView):
    """
    List all event organizers with filtering and sorting.
    
    Filtering:
    - username: Filter by username (partial match)
    - email: Filter by email (partial match)
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, username)
    """
    queryset = models.User.objects.filter(role='event_organizer')
    serializer_class = AdminListEventOrganizerSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    filterset_class = filters.UserFilter
    search_fields = ['username', 'email']
    ordering_fields = ['created_at', 'username', 'email']
    ordering = ['-created_at']

class AdminEventProposalListView(generics.ListAPIView):
    """
    List all event proposals for admin review.
    
    Filtering:
    - status: Filter by proposal status (pending, approved, rejected)
    - category: Filter by event category
    - organizer: Filter by organizer username
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, title)
    """
    queryset = models.Event.objects.all()
    serializer_class = AdminListEventProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    filterset_class = filters.EventFilter
    search_fields = ['title', 'description', 'organizer__username']
    ordering_fields = ['created_at', 'title', 'start_date']
    ordering = ['-created_at']

class AdminEventProposalConfirmView(generics.UpdateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = AdminEventProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

class AdminEventProposalDetailView(generics.RetrieveAPIView):
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

class EventOrganizerProposalCreateView(generics.CreateAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=self.request.user, status='pending')

class EventOrganizerProposalListView(generics.ListAPIView):
    """
    List event organizer proposals for the authenticated user.
    
    Filtering:
    - status: Filter by proposal status (pending, approved, rejected)
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, name)
    """
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    filterset_class = filters.EventOrganizerProposalFilter
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)

class EventOrganizerProposalDetailView(generics.RetrieveAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    lookup_field = 'id'
    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)
    
class AdminEventOrganizerProposalListView(generics.ListAPIView):
    """
    List all event organizer proposals for admin review.
    
    Filtering:
    - status: Filter by proposal status (pending, approved, rejected)
    - organizer: Filter by organizer ID
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, name)
    """
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = AdminListEventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    filterset_class = filters.EventOrganizerProposalFilter
    search_fields = ['name', 'organizer__username', 'description']
    ordering_fields = ['created_at', 'name', 'status']
    ordering = ['-created_at']

class AdminEventOrganizerProposalConfirmView(generics.UpdateAPIView):
    """
    Approve or reject an event organizer proposal.
    When approved, updates the user's role to 'event_organizer'.
    """
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = AdminEventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'approved':
            user = instance.organizer
            user.role = 'event_organizer'
            user.save()
            logger.info(f"User {user.username} approved as event organizer")

class AdminEventOrganizerProposalDetailView(generics.RetrieveAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'


class AccountView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserUpdateSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class AccountDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserUpdateSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'
    
class EventUserListView(generics.ListAPIView):
    """
    List users registered for a specific event.
    
    Filtering:
    - ticket_type: Filter by ticket type
    - customer: Filter by customer ID
    
    Sorting:
    - ordering: Sort by any field (e.g., -created_at, price)
    
    PERFORMANCE: Uses select_related to avoid N+1 queries.
    """
    serializer_class = UserTicketSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    filterset_class = filters.UserTicketFilter
    ordering_fields = ['created_at', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        # PERFORMANCE: Use select_related to join related tables
        event_id = self.kwargs.get('id')
        if event_id is not None:
            return models.UserTicket.objects.select_related(
                'customer', 'ticket', 'event'
            ).filter(ticket__event_id=event_id)
        return models.UserTicket.objects.none()