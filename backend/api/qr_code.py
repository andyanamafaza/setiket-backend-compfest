"""
QR Code generation utilities for tickets.
"""
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import base64
import logging

logger = logging.getLogger(__name__)


class QRCodeService:
    """
    Service for generating QR codes for tickets.
    """
    
    @staticmethod
    def generate_qr_code(user_ticket_id, event_title, ticket_title):
        """
        Generate a QR code for a ticket.
        
        Args:
            user_ticket_id: UUID of the UserTicket
            event_title: Title of the event
            ticket_title: Title of the ticket
            
        Returns:
            str: Base64 encoded QR code data or URL-safe string
        """
        try:
            # Create QR code data
            qr_data = f"SETIKET|{user_ticket_id}|{event_title}|{ticket_title}"
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            logger.error(f"Failed to generate QR code for ticket {user_ticket_id}: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def generate_qr_code_string(user_ticket_id):
        """
        Generate a simple QR code string (URL-safe).
        
        Args:
            user_ticket_id: UUID of the UserTicket
            
        Returns:
            str: QR code string
        """
        return f"SETIKET-{user_ticket_id}"

