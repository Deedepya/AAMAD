# Storage Utility
# Handles document storage (local for MVP, S3/GCP for production)

import os
from pathlib import Path
from typing import Optional
import logging

# Import boto3 only if needed (optional dependency)
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None  # Placeholder to prevent NameError

logger = logging.getLogger(__name__)


class StorageManager:
    """Manages document storage (local or cloud)"""
    
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "local")  # local, s3, gcp
        self.upload_dir = Path(os.getenv("UPLOAD_DIR", "./uploads"))
        
        if self.storage_type == "s3":
            if not BOTO3_AVAILABLE:
                logger.warning("S3 storage requested but boto3 not installed. Falling back to local storage.")
                logger.warning("Install boto3 with: pip install boto3")
                self.storage_type = "local"  # Fallback to local
            else:
                try:
                    self.s3_client = boto3.client(
                        "s3",
                        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name=os.getenv("AWS_REGION", "us-east-1")
                    )
                    self.s3_bucket = os.getenv("S3_BUCKET_NAME", "onboarding-documents")
                except Exception as e:
                    logger.warning(f"Failed to initialize S3 client: {e}. Falling back to local storage.")
                    self.storage_type = "local"
    
    def save_file(self, file_content: bytes, file_name: str, user_id: str) -> str:
        """
        Save file to storage.
        
        Args:
            file_content: File content as bytes
            file_name: Original file name
            user_id: User ID for organizing files
            
        Returns:
            Path to saved file (local path or S3 key)
        """
        if self.storage_type == "local":
            return self._save_local(file_content, file_name, user_id)
        elif self.storage_type == "s3":
            return self._save_s3(file_content, file_name, user_id)
        else:
            raise ValueError(f"Unsupported storage type: {self.storage_type}")
    
    def _save_local(self, file_content: bytes, file_name: str, user_id: str) -> str:
        """Save file to local storage"""
        # Create user directory
        user_dir = self.upload_dir / user_id
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Save file
        file_path = user_dir / file_name
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        logger.info(f"File saved locally: {file_path}")
        return str(file_path)
    
    def _save_s3(self, file_content: bytes, file_name: str, user_id: str) -> str:
        """Save file to S3"""
        if not BOTO3_AVAILABLE:
            logger.error("S3 storage requested but boto3 not available. Cannot save to S3.")
            raise ImportError("boto3 is required for S3 storage. Install with: pip install boto3")
        
        s3_key = f"{user_id}/{file_name}"
        
        try:
            self.s3_client.put_object(
                Bucket=self.s3_bucket,
                Key=s3_key,
                Body=file_content
            )
            logger.info(f"File saved to S3: {s3_key}")
            return s3_key
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            raise
    
    def get_file_url(self, file_path: str, expires_in: int = 3600) -> Optional[str]:
        """
        Get URL to access file (for S3, generates pre-signed URL).
        
        Args:
            file_path: Path to file (local path or S3 key)
            expires_in: URL expiration time in seconds (for S3)
            
        Returns:
            URL to access file
        """
        if self.storage_type == "local":
            # For local storage, return file path (in production, serve via API)
            return file_path
        elif self.storage_type == "s3":
            if not BOTO3_AVAILABLE:
                logger.error("S3 storage requested but boto3 not available.")
                return None
            try:
                url = self.s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.s3_bucket, "Key": file_path},
                    ExpiresIn=expires_in
                )
                return url
            except Exception as e:
                logger.error(f"Failed to generate S3 URL: {str(e)}")
                return None
        else:
            return None


# Global storage manager instance
_storage_manager: Optional[StorageManager] = None


def get_storage_manager() -> StorageManager:
    """Get global storage manager instance"""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = StorageManager()
    return _storage_manager

