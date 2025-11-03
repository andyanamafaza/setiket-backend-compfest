from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .health import health_check
from .views import (
    RegisterUserView,
    LogoutView,
    CustomerEventRetrieveView,
    CustomerEventListView,
    CustomerUpcomingEventListView,
    TicketCreateView,
    TicketPurchaseView,
    AccountView,
    AccountDetailView,
    EventListOwnerView,
    EventCreateView,
    EventUpdateView,
    EventSalesDataView,
    EventUserListView,
    EventOrganizerProposalCreateView,
    EventOrganizerProposalListView,
    EventOrganizerProposalDetailView,
    AdminListUserView,
    AdminListEventOrganizerView,
    AdminEventOrganizerDetailListView,
    AdminEventProposalListView,
    AdminEventProposalConfirmView,
    AdminEventProposalDetailView,
    AdminEventOrganizerProposalListView,
    AdminEventOrganizerProposalConfirmView,
    AdminEventOrganizerProposalDetailView,
)
from .refund_views import RefundTicketView, AdminRefundTicketView
from .qr_code_views import TicketQRCodeView

urlpatterns = [
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # Authentication
    path('auth/login/', TokenObtainPairView.as_view(), name='api_token_auth'),
    path('auth/register/', RegisterUserView.as_view(), name='api_token_register'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('auth/logout/', LogoutView.as_view(), name='api_token_logout'),

    # Event Views
    path('event/<uuid:id>/', CustomerEventRetrieveView.as_view(), name='event_retrieve'),
    path('event/',CustomerEventListView.as_view(), name='event_list'),
    path('event/upcoming/', CustomerUpcomingEventListView.as_view(), name='event_upcoming_list'),

    # Ticket Views
    path('ticket/create/',TicketCreateView.as_view(),name='ticket_create'),
    path('ticket/purchase/',TicketPurchaseView.as_view(),name='ticket_purchase'),
    path('ticket/<uuid:id>/refund/', RefundTicketView.as_view(), name='ticket_refund'),
    path('ticket/<uuid:id>/qr/', TicketQRCodeView.as_view(), name='ticket_qr'),
    
    # Admin Refund
    path('admin/ticket/<uuid:id>/refund/', AdminRefundTicketView.as_view(), name='admin_ticket_refund'),

    # account
    path('account/', AccountView.as_view(), name='account'),
    path('account/<uuid:id>/', AccountDetailView.as_view(), name='account_detail'),


    #Event Organizer Views
    path('event-organizer/ownevent/', EventListOwnerView.as_view(), name='event_own_list'),
    path('event-organizer/event/create/', EventCreateView.as_view(), name='event_create'),
    path('event-organizer/event/update/<uuid:id>/', EventUpdateView.as_view(), name='event_update'),
    path('event-organizer/sales-data/', EventSalesDataView.as_view(), name='event_sales_data'),
    path('event-users/<uuid:id>/', EventUserListView.as_view(), name='event-users-list'),


    # Event Organizer Proposals
    path('event-organizer-proposal/create/', EventOrganizerProposalCreateView.as_view(), name='event_organizer_proposal_create'),
    path('event-organizer-proposal/<uuid:id>/', EventOrganizerProposalDetailView.as_view(), name='event_organizer_proposal_detail'),
    path('event-organizer-proposal/', EventOrganizerProposalListView.as_view(), name='event_organizer_proposal_list'),
    
    # Admin User and Event Organizer Views
    path('admin/user-list/', AdminListUserView.as_view(), name='admin_user_list'),
    path('admin/event-organizers-list/', AdminListEventOrganizerView.as_view(), name='admin_event_organizers'),
    path('admin/event-organizers/<uuid:id>/events/', AdminEventOrganizerDetailListView.as_view(), name='admin_event_organizer_detail_List'),
    
    # Admin Event Proposals
    path('admin/event-proposals/', AdminEventProposalListView.as_view(), name='admin_event_proposal_list'),
    path('admin/event-proposals/<uuid:id>/confirm/', AdminEventProposalConfirmView.as_view(), name='event_proposal_confirm'),
    path('admin/event-proposals/<uuid:id>/', AdminEventProposalDetailView.as_view(), name='event_proposal_detail'),

    # Admin Event Organizer Proposals
    path('admin/event-organizer-proposals/', AdminEventOrganizerProposalListView.as_view(), name='admin_event_organizer_proposal_list'),
    path('admin/event-organizer-proposals/<uuid:id>/confirm/', AdminEventOrganizerProposalConfirmView.as_view(), name='admin_event_proposal_confirm'),
    path('admin/event-organizer-proposals/<uuid:id>/', AdminEventOrganizerProposalDetailView.as_view(), name='admin_event_proposal_detail'),
]
