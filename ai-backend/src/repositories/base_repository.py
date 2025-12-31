"""Base repository class with common CRUD operations."""

from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from uuid import UUID

from pydantic import BaseModel

from src.database import SupabaseClient


T = TypeVar("T", bound=BaseModel)
CreateT = TypeVar("CreateT", bound=BaseModel)
UpdateT = TypeVar("UpdateT", bound=BaseModel)


class BaseRepository(Generic[T, CreateT, UpdateT]):
    """Base repository with common CRUD operations using Supabase REST API."""

    def __init__(
        self,
        supabase_client: SupabaseClient,
        table_name: str,
        model_class: Type[T],
    ):
        """Initialize repository.
        
        Args:
            supabase_client: Supabase client instance
            table_name: Name of the database table
            model_class: Pydantic model class for the entity
        """
        self.supabase = supabase_client
        self.table_name = table_name
        self.model_class = model_class

    def _sanitize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize data by removing None values and converting types.
        
        Args:
            data: Raw data dictionary
            
        Returns:
            Sanitized data dictionary
        """
        return {k: v for k, v in data.items() if v is not None}

    async def create(self, data: CreateT, use_service_role: bool = False) -> T:
        """Create a new record.
        
        Args:
            data: Data for creating the record
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Created record
            
        Raises:
            Exception: If creation fails
        """
        try:
            # Convert Pydantic model to dict
            data_dict = data.model_dump(exclude_unset=True)
            data_dict = self._sanitize_data(data_dict)
            
            # Insert into Supabase
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .insert(data_dict)
                .execute()
            )
            
            if not response.data:
                raise Exception(f"Failed to create {self.table_name} record")
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error creating {self.table_name}: {str(e)}")

    async def get_by_id(self, record_id: UUID, use_service_role: bool = False) -> Optional[T]:
        """Get a record by ID.
        
        Args:
            record_id: ID of the record
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Record if found, None otherwise
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .select("*")
                .eq("id", str(record_id))
                .execute()
            )
            
            if not response.data:
                return None
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error fetching {self.table_name} by ID: {str(e)}")

    async def get_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        use_service_role: bool = False,
    ) -> List[T]:
        """Get all records with optional pagination.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of records
        """
        try:
            query = self.supabase.table(self.table_name, use_service_role).select("*")
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            response = query.execute()
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error fetching all {self.table_name}: {str(e)}")

    async def update(
        self,
        record_id: UUID,
        data: UpdateT,
        use_service_role: bool = False,
    ) -> Optional[T]:
        """Update a record.
        
        Args:
            record_id: ID of the record to update
            data: Update data
            use_service_role: Whether to use service role for the operation
            
        Returns:
            Updated record if found, None otherwise
        """
        try:
            # Convert Pydantic model to dict, excluding unset fields
            data_dict = data.model_dump(exclude_unset=True)
            data_dict = self._sanitize_data(data_dict)
            
            if not data_dict:
                # No fields to update
                return await self.get_by_id(record_id, use_service_role)
            
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .update(data_dict)
                .eq("id", str(record_id))
                .execute()
            )
            
            if not response.data:
                return None
            
            return self.model_class(**response.data[0])
        except Exception as e:
            raise Exception(f"Error updating {self.table_name}: {str(e)}")

    async def delete(self, record_id: UUID, use_service_role: bool = False) -> bool:
        """Delete a record.
        
        Args:
            record_id: ID of the record to delete
            use_service_role: Whether to use service role for the operation
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            response = (
                self.supabase.table(self.table_name, use_service_role)
                .delete()
                .eq("id", str(record_id))
                .execute()
            )
            
            return len(response.data) > 0
        except Exception as e:
            raise Exception(f"Error deleting {self.table_name}: {str(e)}")

    async def filter_by(
        self,
        filters: Dict[str, Any],
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        use_service_role: bool = False,
    ) -> List[T]:
        """Filter records by multiple criteria.
        
        Args:
            filters: Dictionary of field names and values to filter by
            limit: Maximum number of records to return
            offset: Number of records to skip
            use_service_role: Whether to use service role for the operation
            
        Returns:
            List of matching records
        """
        try:
            query = self.supabase.table(self.table_name, use_service_role).select("*")
            
            # Apply filters
            for field, value in filters.items():
                if value is not None:
                    query = query.eq(field, value)
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
            
            response = query.execute()
            
            return [self.model_class(**item) for item in response.data]
        except Exception as e:
            raise Exception(f"Error filtering {self.table_name}: {str(e)}")
