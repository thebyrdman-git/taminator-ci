"""
from typing import Optional
Google Drive Storage API Routes

Cloud-first storage backend using unlimited Drive storage
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from ...core.drive_storage import get_drive_storage
from ...core.token_manager import get_token_manager

router = APIRouter(prefix="/api/drive", tags=["drive-storage"])
logger = logging.getLogger(__name__)


# Models

class DriveFile(BaseModel):
    """Drive file metadata"""
    id: str
    name: str
    mime_type: str
    size: Optional[int]
    modified_time: str
    created_time: str


class StorageQuota(BaseModel):
    """Drive storage quota"""
    total: int
    used: int
    available: int
    unlimited: bool
    user: str


class SyncStatus(BaseModel):
    """Sync operation status"""
    success: bool
    direction: str  # "local_to_drive" or "drive_to_local"
    files_synced: int
    message: str


# Endpoints

@router.get("/status")
async def get_drive_status():
    """
    Get Drive integration status
    
    Returns:
        Drive authentication and setup status
    """
    logger.info("📊 Getting Drive status")
    
    try:
        drive = get_drive_storage()
        
        # Try to access Drive
        quota = drive.get_storage_quota()
        
        return {
            "enabled": True,
            "authenticated": True,
            "quota": quota,
            "folder_structure": "initialized"
        }
    
    except ValueError as e:
        # Not authenticated
        return {
            "enabled": False,
            "authenticated": False,
            "message": str(e)
        }
    
    except Exception as e:
        logger.error(f"❌ Drive status check failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "drive_status_failed", "message": str(e)}
        )


@router.post("/initialize")
async def initialize_drive_structure():
    """
    Initialize Taminator folder structure in Drive
    
    Creates:
    - Taminator/
    - Taminator/customers/
    - Taminator/settings/
    - Taminator/templates/
    
    Returns:
        Folder IDs
    """
    logger.info("🏗️  Initializing Drive structure")
    
    try:
        drive = get_drive_storage()
        structure = drive.initialize_structure()
        
        return {
            "success": True,
            "folders": structure,
            "message": "Drive structure initialized"
        }
    
    except Exception as e:
        logger.error(f"❌ Drive initialization failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "drive_init_failed", "message": str(e)}
        )


@router.get("/quota", response_model=StorageQuota)
async def get_storage_quota():
    """
    Get Drive storage quota
    
    Returns:
        Storage usage information
    """
    logger.info("💾 Getting storage quota")
    
    try:
        drive = get_drive_storage()
        quota = drive.get_storage_quota()
        
        return StorageQuota(**quota)
    
    except Exception as e:
        logger.error(f"❌ Failed to get quota: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "quota_failed", "message": str(e)}
        )


@router.get("/list", response_model=List[DriveFile])
async def list_drive_files(path: str = ""):
    """
    List files in Drive folder
    
    Args:
        path: Folder path relative to Taminator/ (e.g., "customers/td-bank")
        
    Returns:
        List of files in folder
    """
    logger.info(f"📋 Listing Drive files: {path}")
    
    try:
        drive = get_drive_storage()
        files = drive.list_files(path)
        
        return [
            DriveFile(
                id=f['id'],
                name=f['name'],
                mime_type=f['mimeType'],
                size=int(f.get('size', 0)) if f.get('size') else None,
                modified_time=f['modifiedTime'],
                created_time=f['createdTime']
            )
            for f in files
        ]
    
    except Exception as e:
        logger.error(f"❌ Failed to list files: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "list_failed", "message": str(e)}
        )


@router.post("/sync/local-to-drive", response_model=SyncStatus)
async def sync_local_to_drive(background_tasks: BackgroundTasks):
    """
    Sync local customer data to Drive
    
    Uploads:
    - ~/Documents/rh/* → Drive://Taminator/customers/*
    
    Returns:
        Sync status
    """
    logger.info("📤 Starting local → Drive sync")
    
    try:
        drive = get_drive_storage()
        
        # Run sync in foreground (can be moved to background for large datasets)
        drive.sync_from_local()
        
        return SyncStatus(
            success=True,
            direction="local_to_drive",
            files_synced=0,  # TODO: Count files
            message="Local data synced to Drive"
        )
    
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "sync_failed", "message": str(e)}
        )


@router.post("/sync/drive-to-local", response_model=SyncStatus)
async def sync_drive_to_local(background_tasks: BackgroundTasks):
    """
    Sync Drive data to local filesystem
    
    Downloads:
    - Drive://Taminator/customers/* → ~/Documents/rh/*
    
    Returns:
        Sync status
    """
    logger.info("📥 Starting Drive → local sync")
    
    try:
        drive = get_drive_storage()
        
        # Run sync in foreground
        drive.sync_to_local()
        
        return SyncStatus(
            success=True,
            direction="drive_to_local",
            files_synced=0,  # TODO: Count files
            message="Drive data synced to local"
        )
    
    except Exception as e:
        logger.error(f"❌ Sync failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "sync_failed", "message": str(e)}
        )


@router.post("/upload")
async def upload_file(
    drive_path: str,
    file: UploadFile = File(...)
):
    """
    Upload file to Drive
    
    Args:
        drive_path: Destination path in Drive (e.g., "customers/td-bank/report.md")
        file: File to upload
        
    Returns:
        File ID
    """
    logger.info(f"⬆️  Uploading file: {file.filename} → {drive_path}")
    
    try:
        drive = get_drive_storage()
        
        # Save uploaded file temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Upload to Drive
        from pathlib import Path
        file_id = drive.upload_file(
            Path(tmp_path),
            drive_path,
            mime_type=file.content_type
        )
        
        # Cleanup temp file
        Path(tmp_path).unlink()
        
        return {
            "success": True,
            "file_id": file_id,
            "drive_path": drive_path,
            "message": f"File uploaded: {file.filename}"
        }
    
    except Exception as e:
        logger.error(f"❌ Upload failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "upload_failed", "message": str(e)}
        )


@router.get("/download/{path:path}")
async def download_file(path: str):
    """
    Download file from Drive
    
    Args:
        path: File path in Drive (e.g., "customers/td-bank/customer.yaml")
        
    Returns:
        File content
    """
    logger.info(f"⬇️  Downloading file: {path}")
    
    try:
        drive = get_drive_storage()
        content = drive.download_file(path)
        
        from fastapi.responses import Response
        return Response(
            content=content,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={path.split('/')[-1]}"}
        )
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail={"error": "file_not_found", "message": f"File not found: {path}"}
        )
    
    except Exception as e:
        logger.error(f"❌ Download failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "download_failed", "message": str(e)}
        )


@router.delete("/delete/{path:path}")
async def delete_file(path: str):
    """
    Delete file from Drive
    
    Args:
        path: File path in Drive
        
    Returns:
        Success confirmation
    """
    logger.info(f"🗑️  Deleting file: {path}")
    
    try:
        drive = get_drive_storage()
        drive.delete_file(path)
        
        return {
            "success": True,
            "message": f"File deleted: {path}"
        }
    
    except Exception as e:
        logger.error(f"❌ Delete failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "delete_failed", "message": str(e)}
        )

