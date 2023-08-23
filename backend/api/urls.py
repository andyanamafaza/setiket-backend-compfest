from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import *


urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(),name='api_token_auth'),
    path('auth/register/', RegisterUserView.as_view(),name='api_token_register'),
    path('auth/refresh/', TokenRefreshView.as_view(),name='api_token_refresh'),
    path('auth/logout/', LogoutView.as_view(),name='api_token_logout'),
    path('event/<uuid:id>/',EventRetreiveView.as_view(),name='event_retreive'),
    path('event/update/<uuid:id>/',EventUpdateView.as_view(),name='event_update'),
    path('event/',EventListView.as_view(),name='event_list'),
    path('ownevent/',EventListOwnerView.as_view(),name='event_own_list'),
    path('event/create/',EventCreateView.as_view(),name='event_create'),
    path('admin/user-list/', AdminListUserView.as_view(), name='admin_user_list'),
    path('admin/event-organizers-list/', AdminListEventOrganizerView.as_view(), name='admin_event_organizers'),
    path('admin/event-organizers/<uuid:id>/events/', AdminEventOrganizerDetailListView.as_view(), name='admin_event_organizer_detail_List'),
    path('admin/event-proposals/', AdminEventProposalListView.as_view(), name='admin_event_proposal_list'),
    path('admin/event-proposals/<uuid:id>/confirm/', AdminEventProposalConfirmView.as_view(), name='event_proposal_confirm'),
    path('admin/event-proposals/<uuid:id>/', AdminEventProposalDetailView.as_view(), name='event_proposal_detail'),
    path('event-organizer-proposal/create', EventOrganizerProposalCreateView.as_view(), name='event_organizer_proposal_create'),
    path('event-organizer-proposal/<uuid:id>/', EventOrganizerProposalDetailView.as_view(), name='event_organizer_proposal_detail'),
    path('event-organizer-proposal/', EventOrganizerProposalListView.as_view(), name='event_organizer_proposal_list'),
    path('admin/event-organizer-proposals/', AdminEventOrganizerProposalListView.as_view(), name='admin_event_organizer_proposal_list'),
    path('admin/event-organizer-proposals/<uuid:id>/confirm/', AdminEventOrganizerProposalConfirmView.as_view(), name='admin_event_proposal_confirm'),
    path('admin/event-organizer-proposals/<uuid:id>/', AdminEventOrganizerProposalDetailView.as_view(), name='admin_event_proposal_detail'),
]

