"""
Refund views and endpoints.
"""
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from . import models
from .services import RefundService
from . import permissions as custom_permissions
import logging

logger = logging.getLogger(__name__)


class RefundTicketView(generics.DestroyAPIView):
    """
    Refund a ticket.
    Only the ticket owner can request a refund.
    Cannot refund tickets for past events.
    """
    queryset = models.UserTicket.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """
        Process ticket refund.
        """
        try:
            user_ticket = self.get_object()
            
            # Check if user owns the ticket
            if user_ticket.customer != request.user:
                return Response(
                    {'error': 'You do not have permission to refund this ticket.'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Get reason from request data
            reason = request.data.get('reason', None)
            
            # Process refund
            RefundService.refund_ticket(user_ticket.id, reason=reason)
            
            return Response(
                {'message': 'Ticket refunded successfully. The amount has been added to your balance.'},
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            logger.warning(f"Refund failed: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error during refund: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while processing the refund. Please try again.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_queryset(self):
        """Only return tickets owned by the current user."""
        return models.UserTicket.objects.filter(customer=self.request.user)


class AdminRefundTicketView(generics.DestroyAPIView):
    """
    Admin endpoint to refund any ticket.
    """
    queryset = models.UserTicket.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [custom_permissions.IsAdministrator]
    lookup_field = 'id'
    
    def destroy(self, request, *args, **kwargs):
        """
        Process ticket refund (admin).
        """
        try:
            user_ticket = self.get_object()
            reason = request.data.get('reason', None)
            
            RefundService.refund_ticket(user_ticket.id, reason=reason)
            
            return Response(
                {'message': 'Ticket refunded successfully.'},
                status=status.HTTP_200_OK
            )
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error during admin refund: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An error occurred while processing the refund.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

