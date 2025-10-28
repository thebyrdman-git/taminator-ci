"""
Google Drive Storage Backend - Cloud-First Architecture

Replace local filesystem with Google Drive:
- Unlimited storage (Red Hat Workspace)
- Automatic multi-device sync
- Built-in version history
- Team sharing capabilities
- Automatic backup
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime
import io

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from .google_auth import get_google_auth_manager
from .token_manager import get_token_manager

logger = logging.getLogger(__name__)


class DriveStorageManager:
    """
    Google Drive storage backend
    
    Features:
    - Replaces ~/Documents/rh/ with Drive folder
    - Automatic sync across devices
    - Version history (Drive native)
    - Team folder sharing
    - Unlimited storage
    - Offline cache for speed
    
    Structure:
    Taminator/
    ├── customers/
    │   ├── td-bank/
    │   │   ├── customer.yaml
    │   │   └── reports/
    │   │       ├── 2025-10-rfe-bug-report.md
    │   │       └── 2025-09-rfe-bug-report.md
    │   └── wells-fargo/
    │       └── ...
    ├── settings/
    │   └── settings.json (synced across devices)
    └── templates/
        └── report-templates/
    """
    
    # Drive folder structure
    ROOT_FOLDER = "Taminator"
    CUSTOMERS_FOLDER = "customers"
    SETTINGS_FOLDER = "settings"
    TEMPLATES_FOLDER = "templates"
    
    def __init__(self, token_manager=None, use_cache: bool = True):
        """
        Initialize Drive Storage Manager
        
        Args:
            token_manager: TokenManager instance
            use_cache: Use local cache for faster reads
        """
        self.token_manager = token_manager or get_token_manager()
        self.use_cache = use_cache
        
        # Local cache directory
        if use_cache:
            import platformdirs
            self.cache_dir = Path(platformdirs.user_cache_dir("taminator", "redhat")) / "drive"
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Folder ID cache
        self._folder_cache: Dict[str, str] = {}
        
        logger.info("☁️  DriveStorageManager initialized")
    
    def _get_drive_service(self):
        """Get authenticated Google Drive service"""
        auth_manager = get_google_auth_manager(self.token_manager)
        
        if not auth_manager.has_valid_token():
            raise ValueError("Not authenticated with Google. Please sign in first.")
        
        return auth_manager.get_drive_service()
    
    def _ensure_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Ensure folder exists, create if not
        
        Args:
            folder_name: Folder name
            parent_id: Parent folder ID (None = root)
            
        Returns:
            Folder ID
        """
        # Check cache
        cache_key = f"{parent_id}:{folder_name}"
        if cache_key in self._folder_cache:
            return self._folder_cache[cache_key]
        
        drive = self._get_drive_service()
        
        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"
        
        results = drive.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()
        
        files = results.get('files', [])
        
        if files:
            folder_id = files[0]['id']
            logger.debug(f"📁 Found folder: {folder_name} ({folder_id})")
        else:
            # Create folder
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = drive.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder['id']
            logger.info(f"✅ Created folder: {folder_name} ({folder_id})")
        
        # Cache folder ID
        self._folder_cache[cache_key] = folder_id
        return folder_id
    
    def initialize_structure(self):
        """Create Taminator folder structure in Drive"""
        logger.info("🏗️  Initializing Drive folder structure")
        
        # Create root folder
        root_id = self._ensure_folder(self.ROOT_FOLDER)
        
        # Create subfolders
        customers_id = self._ensure_folder(self.CUSTOMERS_FOLDER, root_id)
        settings_id = self._ensure_folder(self.SETTINGS_FOLDER, root_id)
        templates_id = self._ensure_folder(self.TEMPLATES_FOLDER, root_id)
        
        logger.info(f"✅ Drive structure initialized")
        return {
            "root": root_id,
            "customers": customers_id,
            "settings": settings_id,
            "templates": templates_id
        }
    
    def upload_file(
        self,
        local_path: Path,
        drive_path: str,
        mime_type: str = None
    ) -> str:
        """
        Upload file to Drive
        
        Args:
            local_path: Local file path
            drive_path: Drive path (relative to Taminator/)
            mime_type: MIME type (auto-detect if None)
            
        Returns:
            File ID
        """
        logger.info(f"⬆️  Uploading: {local_path} → {drive_path}")
        
        drive = self._get_drive_service()
        
        # Parse drive path
        parts = drive_path.split('/')
        filename = parts[-1]
        folder_path = parts[:-1]
        
        # Ensure folder structure exists
        root_id = self._ensure_folder(self.ROOT_FOLDER)
        current_folder_id = root_id
        
        for folder in folder_path:
            current_folder_id = self._ensure_folder(folder, current_folder_id)
        
        # Check if file exists (update instead of create)
        existing_file_id = self._find_file(filename, current_folder_id)
        
        # Prepare file metadata
        file_metadata = {
            'name': filename,
        }
        
        if not existing_file_id:
            file_metadata['parents'] = [current_folder_id]
        
        # Upload file
        media = MediaFileUpload(
            str(local_path),
            mimetype=mime_type,
            resumable=True
        )
        
        if existing_file_id:
            # Update existing file
            file = drive.files().update(
                fileId=existing_file_id,
                media_body=media,
                fields='id'
            ).execute()
            logger.info(f"✅ Updated file: {filename} ({file['id']})")
        else:
            # Create new file
            file = drive.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            logger.info(f"✅ Uploaded file: {filename} ({file['id']})")
        
        return file['id']
    
    def download_file(
        self,
        drive_path: str,
        local_path: Optional[Path] = None
    ) -> bytes:
        """
        Download file from Drive
        
        Args:
            drive_path: Drive path (relative to Taminator/)
            local_path: Local path to save (None = return bytes)
            
        Returns:
            File content as bytes
        """
        logger.info(f"⬇️  Downloading: {drive_path}")
        
        drive = self._get_drive_service()
        
        # Parse drive path
        parts = drive_path.split('/')
        filename = parts[-1]
        folder_path = parts[:-1]
        
        # Navigate to folder
        root_id = self._ensure_folder(self.ROOT_FOLDER)
        current_folder_id = root_id
        
        for folder in folder_path:
            current_folder_id = self._ensure_folder(folder, current_folder_id)
        
        # Find file
        file_id = self._find_file(filename, current_folder_id)
        
        if not file_id:
            raise FileNotFoundError(f"File not found in Drive: {drive_path}")
        
        # Download file
        request = drive.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            logger.debug(f"Download {int(status.progress() * 100)}%")
        
        content = fh.getvalue()
        
        # Save to local file if requested
        if local_path:
            local_path.write_bytes(content)
            logger.info(f"✅ Downloaded to: {local_path}")
        
        # Cache locally
        if self.use_cache and local_path is None:
            cache_path = self._get_cache_path(drive_path)
            cache_path.parent.mkdir(parents=True, exist_ok=True)
            cache_path.write_bytes(content)
        
        return content
    
    def _find_file(self, filename: str, parent_id: str) -> Optional[str]:
        """Find file ID in parent folder"""
        drive = self._get_drive_service()
        
        query = f"name='{filename}' and '{parent_id}' in parents and trashed=false"
        
        results = drive.files().list(
            q=query,
            spaces='drive',
            fields='files(id)'
        ).execute()
        
        files = results.get('files', [])
        return files[0]['id'] if files else None
    
    def list_files(self, drive_path: str = "") -> List[Dict[str, Any]]:
        """
        List files in Drive folder
        
        Args:
            drive_path: Folder path (relative to Taminator/)
            
        Returns:
            List of file metadata
        """
        drive = self._get_drive_service()
        
        # Navigate to folder
        root_id = self._ensure_folder(self.ROOT_FOLDER)
        current_folder_id = root_id
        
        if drive_path:
            for folder in drive_path.split('/'):
                current_folder_id = self._ensure_folder(folder, current_folder_id)
        
        # List files
        query = f"'{current_folder_id}' in parents and trashed=false"
        
        results = drive.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name, mimeType, size, modifiedTime, createdTime)',
            orderBy='name'
        ).execute()
        
        return results.get('files', [])
    
    def delete_file(self, drive_path: str):
        """Delete file from Drive"""
        logger.info(f"🗑️  Deleting: {drive_path}")
        
        drive = self._get_drive_service()
        
        # Parse drive path
        parts = drive_path.split('/')
        filename = parts[-1]
        folder_path = parts[:-1]
        
        # Navigate to folder
        root_id = self._ensure_folder(self.ROOT_FOLDER)
        current_folder_id = root_id
        
        for folder in folder_path:
            current_folder_id = self._ensure_folder(folder, current_folder_id)
        
        # Find and delete file
        file_id = self._find_file(filename, current_folder_id)
        
        if file_id:
            drive.files().delete(fileId=file_id).execute()
            logger.info(f"✅ Deleted: {drive_path}")
        else:
            logger.warning(f"⚠️  File not found: {drive_path}")
    
    def _get_cache_path(self, drive_path: str) -> Path:
        """Get local cache path for drive file"""
        return self.cache_dir / drive_path.replace('/', '_')
    
    def sync_from_local(self, local_dir: Path = None):
        """
        Sync local customer data to Drive
        
        Args:
            local_dir: Local directory to sync (default: ~/Documents/rh/)
        """
        if local_dir is None:
            local_dir = Path.home() / "Documents" / "rh"
        
        if not local_dir.exists():
            logger.warning(f"⚠️  Local directory not found: {local_dir}")
            return
        
        logger.info(f"🔄 Syncing local → Drive: {local_dir}")
        
        # Sync each customer folder
        for customer_dir in local_dir.iterdir():
            if not customer_dir.is_dir():
                continue
            
            customer_id = customer_dir.name
            logger.info(f"📤 Syncing customer: {customer_id}")
            
            # Upload customer.yaml
            customer_yaml = customer_dir / "customer.yaml"
            if customer_yaml.exists():
                self.upload_file(
                    customer_yaml,
                    f"customers/{customer_id}/customer.yaml"
                )
            
            # Upload reports
            reports_dir = customer_dir / "reports"
            if reports_dir.exists():
                for report_file in reports_dir.glob("*.md"):
                    self.upload_file(
                        report_file,
                        f"customers/{customer_id}/reports/{report_file.name}"
                    )
        
        logger.info("✅ Sync complete: local → Drive")
    
    def sync_to_local(self, local_dir: Path = None):
        """
        Sync Drive data to local directory
        
        Args:
            local_dir: Local directory to sync to (default: ~/Documents/rh/)
        """
        if local_dir is None:
            local_dir = Path.home() / "Documents" / "rh"
        
        local_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"🔄 Syncing Drive → local: {local_dir}")
        
        # List all customers
        customers = self.list_files("customers")
        
        for customer in customers:
            if customer['mimeType'] != 'application/vnd.google-apps.folder':
                continue
            
            customer_id = customer['name']
            customer_dir = local_dir / customer_id
            customer_dir.mkdir(exist_ok=True)
            
            logger.info(f"📥 Syncing customer: {customer_id}")
            
            # Download customer.yaml
            try:
                content = self.download_file(f"customers/{customer_id}/customer.yaml")
                (customer_dir / "customer.yaml").write_bytes(content)
            except FileNotFoundError:
                logger.warning(f"⚠️  No customer.yaml for {customer_id}")
            
            # Download reports
            reports = self.list_files(f"customers/{customer_id}/reports")
            if reports:
                reports_dir = customer_dir / "reports"
                reports_dir.mkdir(exist_ok=True)
                
                for report in reports:
                    if report['mimeType'] != 'application/vnd.google-apps.folder':
                        content = self.download_file(
                            f"customers/{customer_id}/reports/{report['name']}"
                        )
                        (reports_dir / report['name']).write_bytes(content)
        
        logger.info("✅ Sync complete: Drive → local")
    
    def get_storage_quota(self) -> Dict[str, Any]:
        """Get Drive storage quota information"""
        drive = self._get_drive_service()
        
        about = drive.about().get(fields="storageQuota, user").execute()
        quota = about.get('storageQuota', {})
        
        return {
            "total": int(quota.get('limit', 0)),
            "used": int(quota.get('usage', 0)),
            "available": int(quota.get('limit', 0)) - int(quota.get('usage', 0)),
            "unlimited": quota.get('limit') is None,
            "user": about.get('user', {}).get('emailAddress')
        }


# Global singleton
_drive_storage: Optional[DriveStorageManager] = None


def get_drive_storage() -> DriveStorageManager:
    """Get global DriveStorageManager instance"""
    global _drive_storage
    
    if _drive_storage is None:
        _drive_storage = DriveStorageManager()
    
    return _drive_storage

