"""Database package for Supabase integration."""

from src.database.supabase_client import get_supabase_client, SupabaseClient

__all__ = ["get_supabase_client", "SupabaseClient"]
