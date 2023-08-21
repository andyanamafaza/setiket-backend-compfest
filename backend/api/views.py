from rest_framework import generics,permissions,authentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from . import models
from . import permissions as custom_permissions
from .serializers import EventSerializers,UserSerializers, AdminOverviewRegisteredUser

# Create your views here.
#sessionauth is only development only, later will replace with jwt
class EventRetreiveView(generics.RetrieveAPIView):
    queryset = models.Event.objects.all()
    serializer_class = EventSerializers
    lookup_field = 'id'
    authentication_classes = [authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]


class EventListView(generics.ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

class EventCreateView(generics.CreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrEventOrganizers]

    def perform_create(self,serializer):
        serializer.is_valid(raise_exception=True)
        description = serializer.validated_data.get('description') or 'this is default for content'
        serializer.save(organizer=self.request.user,description=description)

class EventUpdateView(generics.UpdateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = EventSerializers
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdminOrOwner]
    lookup_field = 'id'

    
class EventListOwnerView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializers
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


class LogoutView(generics.GenericAPIView):
    # authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class AdminOverviewRegisteredUser(generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = AdminOverviewRegisteredUser
    authentication_classes = [JWTAuthentication,authentication.TokenAuthentication,authentication.SessionAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]