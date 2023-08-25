from rest_framework import generics, permissions, authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import permissions as custom_permissions
from .serializers import *
from drf_spectacular.utils import extend_schema_view,extend_schema,OpenApiParameter

# Create your views here.
#sessionauth is only development only, later will replace with jwt


class CustomerEventRetreiveView(generics.RetrieveAPIView):
    queryset = models.Event.objects.all()
    serializer_class = CustomerDetailEventSerializers
    lookup_field = 'id'
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]


@extend_schema_view(get=extend_schema(parameters=[OpenApiParameter(name='category', description='Category Name', type=str)]))
class CustomerEventListView(generics.ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = CustomerListEventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsCustomerOrAdmin]
    def get_queryset(self):
        category = self.request.query_params.get('category')
        if category:
            queryset = self.queryset.filter(category=category, status='approved')
            if queryset.exists():
                return queryset
            return []
        return self.queryset.filter(status='approved')

class EventCreateView(generics.CreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        description = serializer.validated_data.get('description') or 'this is default for description'
        serializer.save(organizer=self.request.user, description=description)

class TicketCreateView(generics.CreateAPIView):
    queryset = models.Ticket.objects.all()
    serializer_class = DetailTicketSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

class TicketPurchaseView(generics.CreateAPIView):
    queryset = models.UserTicket.objects.all()
    serializer_class = PurchaseTicketSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

class EventUpdateView(generics.UpdateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrOwner]
    lookup_field = 'id'

class EventListOwnerView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailEventSerializers
    queryset = models.Event.objects.all() # add the queryset variable here
    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user) # use the queryset variable here

class RegisterUserView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'success'},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'message':'logout failed'},status=status.HTTP_400_BAD_REQUEST)
        

class AdminListUserView(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = AdminListUserSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

class AdminEventOrganizerDetailListView(generics.ListAPIView):
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

    def get_queryset(self):
        organizer_id = self.kwargs['id']
        return models.Event.objects.filter(organizer_id=organizer_id)

class AdminListEventOrganizerView(generics.ListAPIView):
    queryset = models.User.objects.filter(role='event_organizer')
    serializer_class = AdminListEventOrganizerSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

class AdminEventProposalListView(generics.ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = AdminListEventProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

class AdminEventProposalConfirmView(generics.UpdateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = AdminEventProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

class AdminEventProposalDetailView(generics.RetrieveAPIView):
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

class EventOrganizerProposalCreateView(generics.CreateAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save(organizer=self.request.user, status='pending')

class EventOrganizerProposalListView(generics.ListAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)

class EventOrganizerProposalDetailView(generics.RetrieveAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
    lookup_field = 'id'
    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user)
    
class AdminEventOrganizerProposalListView(generics.ListAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = AdminListEventProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]

class AdminEventOrganizerProposalConfirmView(generics.UpdateAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = AdminEventProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'approved':
            user = instance.organizer
            user.role = 'event_organizer'
            user.save()

class AdminEventOrganizerProposalDetailView(generics.RetrieveAPIView):
    queryset = models.EventOrganizerProposal.objects.all()
    serializer_class = EventOrganizerProposalSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'


class AccountView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserUpdateSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class AccountDetailView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserUpdateSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'