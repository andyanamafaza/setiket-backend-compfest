"""
QR Code views and endpoints.
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models
from .qr_code import QRCodeService
import logging

logger = logging.getLogger(__name__)


class TicketQRCodeView(generics.RetrieveAPIView):
    """
    Get QR code for a ticket.
    Only the ticket owner can view the QR code.
    """
    queryset = models.UserTicket.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        """
        Return QR code image and data for the ticket.
        """
        user_ticket = self.get_object()
        
        # Check if user owns the ticket
        if user_ticket.customer != request.user:
            return Response(
                {'error': 'You do not have permission to view this ticket.'},
                status=403
            )
        
        # Generate QR code
        qr_code_image = QRCodeService.generate_qr_code(
            str(user_ticket.id),
            user_ticket.event.title,
            user_ticket.ticket.title
        )
        
        return Response({
            'qr_code': qr_code_image,
            'qr_code_string': user_ticket.qr_code,
            'ticket_id': str(user_ticket.id),
            'event': user_ticket.event.title,
            'ticket': user_ticket.ticket.title
        })
    
    def get_queryset(self):
        """Only return tickets owned by the current user."""
        return models.UserTicket.objects.filter(customer=self.request.user)

