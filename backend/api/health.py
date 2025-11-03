"""
Health check endpoint for monitoring and load balancers.
"""
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Health check endpoint.
    Returns 200 if all services are healthy, 503 otherwise.
    """
    health_status = {
        'status': 'healthy',
        'database': 'unknown',
        'version': '1.0.0'
    }
    status_code = 200
    
    # Check database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_status['database'] = 'connected'
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status['database'] = 'disconnected'
        health_status['status'] = 'unhealthy'
        status_code = 503
    
    return JsonResponse(health_status, status=status_code)

