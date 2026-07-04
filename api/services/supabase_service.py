import os
from supabase import create_client, Client
from storage3.exceptions import StorageApiError
import secrets

class SupabaseService:
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL", "")
        key: str = os.environ.get("SUPABASE_ANON_KEY", "")
        
        if not url or not key:
            raise ValueError("Missing SUPABASE_URL or SUPABASE_ANON_KEY environment variables.")
            
        self.client: Client = create_client(url, key)
        
        # Automatically assert and build infrastructure dependencies on startup
        self._ensure_bucket_exists("models")

    def _ensure_bucket_exists(self, bucket_name: str):
        """
        Checks if the requested storage bucket exists. 
        If not found, creates it automatically with public access enabled.
        """
        try:
            # 1. Fetch all existing storage buckets in the project
            buckets = self.client.storage.list_buckets()
            existing_bucket_names = [b.name for b in buckets]
            
            # 2. If our target bucket isn't there, provision it programmatically
            if bucket_name not in existing_bucket_names:
                print(f"⚙️ [INFRASTRUCTURE] Storage bucket '{bucket_name}' not found. Initializing...")
                
                # Create the bucket. We set public=True so the generated model URLs 
                # can be accessed by the developers later for downloads.
                self.client.storage.create_bucket(
                    id=bucket_name, 
                    options={"public": True, "file_size_limit": 52428800} # 50MB limit example
                )
                print(f"🎉 [SUCCESS] Storage bucket '{bucket_name}' provisioned successfully!")
                
        except StorageApiError as e:
            # If it fails due to permissions (e.g., using an anon key without proper RLS policies), log it safely
            print(f"⚠️ [WARNING] Could not verify or create bucket '{bucket_name}': {e.message}")
        except Exception as e:
            print(f"⚠️ [WARNING] Unexpected storage initialization error: {str(e)}")

    def register_user(self, email, password):
        """Creates a new auth account user record profile in Supabase."""
        response = self.client.auth.sign_up({"email": email, "password": password})
        return response

    def login_user(self, email, password):
        """Authenticates user session records credentials."""
        response = self.client.auth.sign_in_with_password({"email": email, "password": password})
        return response

    def upload_to_bucket(self, bucket_name: str, file_path: str, file_data: bytes) -> str:
        """Uploads raw binary bytes payload arrays into storage block locations."""
        self.client.storage.from_(bucket_name).upload(
            path=file_path,
            file=file_data,
            file_options={"content-type": "application/octet-stream", "x-upsert": "true"}
        )
        
        url_res = self.client.storage.from_(bucket_name).get_public_url(file_path)
        return url_res
    
    def save_model_metadata(self, user_id: str, model_name: str, problem_type: str, score: float, storage_url: str) -> dict:
        """
        Generates a secure API key and saves the model's deployment record to PostgreSQL.
        """
        # Generate a distinct commercial-looking API Token: e.g., "sk_engine_7f8a9b..."
        secure_api_key = f"sk_engine_{secrets.token_hex(16)}"
        
        payload = {
            "user_id": user_id,
            "model_name": model_name,
            "problem_type": problem_type,
            "performance_score": float(score),
            "storage_url": storage_url,
            "api_key": secure_api_key
        }
        
        # Insert row into the database registry table
        response = self.client.table("models_registry").insert(payload).execute()
        return response.data[0]

    def get_user_models(self, user_id: str) -> list:
        """
        Fetches all historical machine learning engines trained by a specific user profile.
        """
        response = self.client.table("models_registry").select("*").eq("user_id", user_id).execute()
        return response.data

    def verify_api_key(self, api_key: str) -> dict:
        """
        Validates if an incoming API key header corresponds to an active model.
        """
        response = self.client.table("models_registry").select("*").eq("api_key", api_key).execute()
        if len(response.data) == 0:
            return None
        return response.data[0]