"""Supabase client configuration with async support."""

from functools import lru_cache
from typing import Optional

from supabase import create_client, Client
from postgrest import AsyncPostgrestClient

from src.config import get_settings


class SupabaseClient:
    """Wrapper for Supabase client with async support."""

    def __init__(self, url: str, key: str, service_role_key: Optional[str] = None):
        """Initialize Supabase client.
        
        Args:
            url: Supabase project URL
            key: Supabase anon key
            service_role_key: Optional service role key for admin operations
        """
        self.url = url
        self.key = key
        self.service_role_key = service_role_key
        
        # Create client with anon key (for user-level operations)
        self._client: Client = create_client(url, key)
        
        # Create service role client if key provided (for admin operations)
        self._service_client: Optional[Client] = None
        if service_role_key:
            self._service_client = create_client(url, service_role_key)

    @property
    def client(self) -> Client:
        """Get the standard Supabase client (anon key)."""
        return self._client

    @property
    def service_client(self) -> Optional[Client]:
        """Get the service role client (admin operations)."""
        return self._service_client

    def table(self, table_name: str, use_service_role: bool = False):
        """Get a table reference.
        
        Args:
            table_name: Name of the table
            use_service_role: Whether to use service role client
            
        Returns:
            Table reference for queries
        """
        if use_service_role and self._service_client:
            return self._service_client.table(table_name)
        return self._client.table(table_name)

    def from_(self, table_name: str, use_service_role: bool = False):
        """Alias for table() method for PostgREST compatibility.
        
        Args:
            table_name: Name of the table
            use_service_role: Whether to use service role client
            
        Returns:
            Table reference for queries
        """
        return self.table(table_name, use_service_role)


@lru_cache
def get_supabase_client() -> SupabaseClient:
    """Get cached Supabase client instance.
    
    Returns:
        SupabaseClient instance
        
    Raises:
        ValueError: If Supabase credentials are not configured
    """
    settings = get_settings()
    
    if not settings.supabase_url or not settings.supabase_key:
        raise ValueError(
            "Supabase credentials not configured. "
            "Please set SUPABASE_URL and SUPABASE_KEY environment variables."
        )
    
    return SupabaseClient(
        url=settings.supabase_url,
        key=settings.supabase_key,
        service_role_key=settings.supabase_service_role_key or None,
    )
