from rest_framework import generics,permissions,authentication
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
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
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
            queryset = self.queryset.filter(category=category)
            if queryset.exists():
                return queryset
            return []
        return self.queryset.all()

class EventCreateView(generics.CreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = DetailEventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

    def perform_create(self,serializer):
        serializer.is_valid(raise_exception=True)
        description = serializer.validated_data.get('description') or 'this is default for content'
        serializer.save(organizer=self.request.user,description=description)

class TicketCreateView(generics.CreateAPIView):
    queryset = models.Ticket.objects.all()
    serializer_class = DetailTicketSerializers
    authentication_classes = [JWTAuthentication, authentication.TokenAuthentication, authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]
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
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DetailEventSerializers
    queryset = models.Event.objects.all() # add the queryset variable here
    def get_queryset(self):
        return self.queryset.filter(organizer=self.request.user) # use the queryset variable here


class RegisterUserView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = UserSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]
    def perform_create(self,serializer):
        serializer.is_valid(raise_exception=True)
        serializer.save()


class LogoutView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
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
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]