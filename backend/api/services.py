"""
Service layer for business logic.
Separates business logic from serializers and views for better maintainability.
"""
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from . import models
from .qr_code import QRCodeService
import logging

logger = logging.getLogger(__name__)


class TicketPurchaseService:
    """
    Service class for handling ticket purchases.
    Ensures atomicity and prevents race conditions.
    """
    
    @staticmethod
    @transaction.atomic
    def purchase_ticket(ticket_id, user, price=None):
        """
        Handles the atomic purchase of a ticket.
        Ensures data consistency and prevents race conditions.
        
        Args:
            ticket_id: UUID of the ticket to purchase
            user: User instance purchasing the ticket
            price: Optional price (required for 'relawan' type)
            
        Returns:
            UserTicket instance
            
        Raises:
            ValueError: If ticket not found, insufficient balance, sold out, or invalid price
        """
        try:
            # Lock the ticket row for update
            ticket = models.Ticket.objects.select_for_update().select_related('event', 'event__organizer').get(id=ticket_id)
        except models.Ticket.DoesNotExist:
            raise ValueError('Ticket not found')

        # Determine the final price
        final_price = ticket.price
        if ticket.ticket_type == 'relawan':
            if price is None:
                raise ValueError('Price must be provided for "relawan" ticket type')
            if price < ticket.price:
                raise ValueError('Price must be greater or equal than minimum ticket price')
            final_price = price
        elif ticket.ticket_type == 'free':
            if price is not None and price > 0:
                raise ValueError('Price must be 0 for "free" ticket type')
            final_price = 0
        elif ticket.ticket_type == 'paid':
            if price is not None and price != ticket.price:
                raise ValueError(f'Price must be {ticket.price} for "paid" ticket type')
            final_price = ticket.price

        # Check balance and ticket quantity
        # Lock user balance to prevent concurrent modifications
        user_account = models.User.objects.select_for_update().get(id=user.id)

        if user_account.balance < final_price:
            raise ValueError('Insufficient balance')

        if ticket.ticket_quantity <= 0:
            raise ValueError('Ticket is sold out')

        # Deduct balance
        user_account.balance -= final_price
        user_account.save()

        # Decrement ticket quantity
        ticket.ticket_quantity -= 1
        ticket.save()

        # Get or create sales data (with select_for_update for safety)
        sales_data, created = models.SalesData.objects.select_for_update().get_or_create(
            event=ticket.event,
            defaults={
                'organizer': ticket.event.organizer,
                'amount': 0,
            }
        )
        sales_data.amount += final_price
        sales_data.save()

        # Update event stats (with select_for_update)
        event = models.Event.objects.select_for_update().get(id=ticket.event.id)
        event.total_sales += final_price
        event.total_sold += 1
        event.save()

        # Create user ticket
        user_ticket = models.UserTicket.objects.create(
            customer=user_account,
            ticket=ticket,
            price=final_price,
            event=ticket.event,
            sales_data=sales_data
        )
        
        # Generate and update QR code
        qr_code_string = QRCodeService.generate_qr_code_string(str(user_ticket.id))
        user_ticket.qr_code = qr_code_string
        user_ticket.save()

        # Send email asynchronously (outside transaction if possible, or handle failure gracefully)
        try:
            send_mail(
                subject='Ticket Confirmation For Event ' + ticket.event.title,
                message='Ticket Confirmation For Event ' + ticket.event.title,
                from_email=settings.EMAIL_HOST_SENDER,
                auth_user=settings.EMAIL_HOST_USER,
                recipient_list=[user_account.email],
                auth_password=settings.EMAIL_HOST_PASSWORD,
                html_message=render_to_string(
                    'email_confirmation.html',
                    {
                        'ticket_id': user_ticket.id,
                        'name': user_account.username,
                        'ticket_name': ticket.title,
                        'ticket_event_name': ticket.event.title
                    }
                ),
                fail_silently=True  # Don't fail transaction if email fails
            )
        except Exception as e:
            logger.error(f"Failed to send ticket confirmation email for user {user_account.username}: {str(e)}", exc_info=True)
            # The transaction is already committed, so just log the email failure.

        return user_ticket


class RefundService:
    """
    Service class for handling ticket refunds.
    """
    
    @staticmethod
    @transaction.atomic
    def refund_ticket(user_ticket_id, reason=None):
        """
        Process a ticket refund.
        
        Args:
            user_ticket_id: UUID of the UserTicket to refund
            reason: Optional reason for refund
            
        Returns:
            UserTicket instance (before deletion)
            
        Raises:
            ValueError: If ticket not found, already refunded, or event has passed
        """
        try:
            # Lock user_ticket row to prevent race conditions
            user_ticket = models.UserTicket.objects.select_for_update().select_related(
                'customer', 'ticket', 'event', 'sales_data'
            ).get(id=user_ticket_id)
        except models.UserTicket.DoesNotExist:
            raise ValueError('Ticket not found')
        
        # Check if event has passed (can't refund past events)
        from datetime import datetime
        if user_ticket.event.end_date < datetime.now().date():
            raise ValueError('Cannot refund tickets for past events')
        
        # Store ticket info before deletion
        ticket_info = {
            'customer': user_ticket.customer,
            'ticket': user_ticket.ticket,
            'event': user_ticket.event,
            'price': user_ticket.price
        }
        
        # Refund amount
        refund_amount = user_ticket.price
        
        # Lock customer balance
        customer = models.User.objects.select_for_update().get(id=user_ticket.customer.id)
        
        # Refund to customer balance
        customer.balance += refund_amount
        customer.save()
        
        # Update ticket quantity (restore one ticket)
        ticket = models.Ticket.objects.select_for_update().get(id=user_ticket.ticket.id)
        ticket.ticket_quantity += 1
        ticket.save()
        
        # Update sales data
        if user_ticket.sales_data:
            sales_data = models.SalesData.objects.select_for_update().get(id=user_ticket.sales_data.id)
            sales_data.amount -= refund_amount
            sales_data.save()
        
        # Update event stats
        event = models.Event.objects.select_for_update().get(id=user_ticket.event.id)
        event.total_sales -= refund_amount
        event.total_sold -= 1
        event.save()
        
        # Delete user ticket (or mark as refunded)
        user_ticket.delete()
        
        # Send refund confirmation email
        RefundService._send_refund_email(
            customer, 
            ticket_info['ticket'], 
            ticket_info['event'], 
            refund_amount, 
            reason
        )
        
        logger.info(f"Ticket {user_ticket_id} refunded. Amount: {refund_amount}")
        return user_ticket
    
    @staticmethod
    def _send_refund_email(user, ticket, event, refund_amount, reason):
        """
        Send refund confirmation email.
        """
        try:
            send_mail(
                subject=f'Refund Confirmation - {event.title}',
                message=f'Your ticket has been refunded. Amount: {refund_amount}',
                from_email=settings.EMAIL_HOST_SENDER,
                auth_user=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                auth_password=settings.EMAIL_HOST_PASSWORD,
                html_message=f"""
                <html>
                <body>
                    <h2>Refund Confirmation</h2>
                    <p>Dear {user.username},</p>
                    <p>Your ticket for <strong>{event.title}</strong> has been refunded.</p>
                    <p><strong>Refund Amount:</strong> {refund_amount}</p>
                    <p><strong>Ticket:</strong> {ticket.title}</p>
                    {f'<p><strong>Reason:</strong> {reason}</p>' if reason else ''}
                    <p>The refund has been added to your account balance.</p>
                </body>
                </html>
                """,
                fail_silently=True
            )
        except Exception as e:
            logger.error(f"Failed to send refund email to {user.email}: {str(e)}", exc_info=True)
