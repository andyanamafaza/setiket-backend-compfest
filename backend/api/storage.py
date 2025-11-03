"""
SeaweedFS storage backend for Django.
Handles file uploads and retrieval from SeaweedFS distributed file system.
"""
import requests
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.deconstruct import deconstructible
import os
import logging

logger = logging.getLogger(__name__)


@deconstructible
class SeaweedFSStorage(Storage):
    """
    SeaweedFS storage backend for Django.
    """
    
    def __init__(self, location=None, base_url=None):
        self.location = location or ''
        self.base_url = base_url or getattr(settings, 'SEAWEEDFS_URL', 'http://localhost:8333')
        self.filer_url = getattr(settings, 'SEAWEEDFS_FILER_URL', f'{self.base_url}/filer')
        self.master_url = getattr(settings, 'SEAWEEDFS_MASTER_URL', self.base_url)
    
    def _save(self, name, content):
        """
        Save file to SeaweedFS via Filer API.
        """
        try:
            # Read file content
            if hasattr(content, 'read'):
                # Reset file pointer if needed
                if hasattr(content, 'seek'):
                    content.seek(0)
                file_content = content.read()
            else:
                file_content = content
            
            # Prepare file path in SeaweedFS
            # name already includes the upload_to path (e.g., 'users/filename.jpg')
            filer_path = name if name.startswith('/') else f'/{name}'
            
            # Upload to SeaweedFS Filer
            upload_url = f"{self.filer_url}{filer_path}"
            
            # Determine content type
            content_type = 'application/octet-stream'
            if hasattr(content, 'content_type') and content.content_type:
                content_type = content.content_type
            elif hasattr(content, 'name'):
                import mimetypes
                guessed_type = mimetypes.guess_type(content.name)[0]
                if guessed_type:
                    content_type = guessed_type
            
            # Upload file
            response = requests.put(
                upload_url,
                data=file_content,
                headers={'Content-Type': content_type},
                timeout=30
            )
            response.raise_for_status()
            
            # Return the path for storage in database
            return name
            
        except Exception as e:
            logger.error(f"Error saving file to SeaweedFS: {str(e)}", exc_info=True)
            raise
    
    def _open(self, name, mode='rb'):
        """
        Open file from SeaweedFS.
        """
        try:
            file_url = self.url(name)
            response = requests.get(file_url, timeout=30)
            response.raise_for_status()
            return ContentFile(response.content)
        except Exception as e:
            logger.error(f"Error opening file from SeaweedFS: {str(e)}", exc_info=True)
            raise
    
    def exists(self, name):
        """
        Check if file exists in SeaweedFS.
        """
        try:
            file_url = self.url(name)
            response = requests.head(file_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def url(self, name):
        """
        Return the URL for accessing the file.
        """
        if name.startswith('http://') or name.startswith('https://'):
            return name
        
        # name already includes the path (e.g., 'users/filename.jpg')
        filer_path = name if name.startswith('/') else f'/{name}'
        return f"{self.filer_url}{filer_path}"
    
    def delete(self, name):
        """
        Delete file from SeaweedFS.
        """
        try:
            filer_path = name if name.startswith('/') else f'/{name}'
            delete_url = f"{self.filer_url}{filer_path}"
            response = requests.delete(delete_url, timeout=30)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Error deleting file from SeaweedFS: {str(e)}", exc_info=True)
            raise
    
    def size(self, name):
        """
        Return the file size.
        """
        try:
            file_url = self.url(name)
            response = requests.head(file_url, timeout=10)
            if response.status_code == 200:
                return int(response.headers.get('Content-Length', 0))
            return 0
        except:
            return 0
    
    def path(self, name):
        """
        Return the local file system path (not applicable for SeaweedFS).
        """
        raise NotImplementedError("SeaweedFS doesn't support local file paths")
