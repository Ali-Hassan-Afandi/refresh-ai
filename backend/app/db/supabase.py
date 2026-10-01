from functools import lru_cache
from supabase import create_client, Client
from app.core.config import settings
@lru_cache
def get_supabase()->Client:
    if not settings.supabase_url: raise RuntimeError("SUPABASE_URL is missing")
    if not settings.supabase_service_role_key: raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is missing")
    return create_client(settings.supabase_url,settings.supabase_service_role_key)
