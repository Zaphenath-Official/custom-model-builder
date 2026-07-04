import abc
import io

# 1. THE PORT (Abstract Interface)
class StoragePort(abc.ABC):
    @abc.abstractmethod
    def upload_model_file(self, user_id: str, model_name: str, file_bytes: io.BytesIO) -> str:
        """Should upload binary file stream and return the public storage access URL string."""
        pass

# 2. THE ADAPTER (Specific Cloud Implementation)
class SupabaseStorageAdapter(StoragePort):
    def __init__(self, supabase_service):
        # Pass your custom supabase service instance into the initialization setup
        self.service = supabase_service

    def upload_model_file(self, user_id: str, model_name: str, file_bytes: io.BytesIO) -> str:
        # Sanitize filename string variables safely
        safe_filename = f"{user_id}/{model_name.replace(' ', '_')}.joblib"
        
        # Reset byte buffer read index boundary
        file_bytes.seek(0)
        
        # Forward the action straight to your underlying cloud client wrapper execution
        public_url = self.service.upload_to_bucket(
            bucket_name="models",
            file_path=safe_filename,
            file_data=file_bytes.read()
        )
        return public_url