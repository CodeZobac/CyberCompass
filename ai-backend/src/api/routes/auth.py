"""Authentication routes."""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.middleware import create_access_token, get_current_user, verify_password
from src.config import get_settings
from src.models import LoginRequest, SuccessResponse, TokenResponse

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest) -> TokenResponse:
    """
    Authenticate user and return JWT token.

    This is a placeholder implementation. In production, you would:
    1. Query the database for the user
    2. Verify the password hash
    3. Return appropriate errors for invalid credentials

    Args:
        request: Login credentials

    Returns:
        JWT access token

    Raises:
        HTTPException: If credentials are invalid
    """
    # TODO: Replace with actual database lookup
    # This is a placeholder for demonstration
    # In production, query your user database here

    # For now, we'll create a token with the email as the subject
    # In production, use the actual user_id from database
    token_data = {
        "sub": request.email,  # In production: user.id
        "email": request.email,
        "roles": ["user"],  # In production: user.roles
        "locale": "en",  # In production: user.locale
    }

    access_token = create_access_token(
        data=token_data,
        expires_delta=timedelta(minutes=settings.jwt_expiration_minutes),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.jwt_expiration_minutes * 60,
    )


@router.get("/me", response_model=SuccessResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)) -> SuccessResponse:
    """
    Get current authenticated user information.

    Args:
        current_user: Current user from JWT token

    Returns:
        User information
    """
    return SuccessResponse(
        message="User information retrieved successfully",
        data=current_user,
    )


@router.post("/logout", response_model=SuccessResponse)
async def logout(current_user: dict = Depends(get_current_user)) -> SuccessResponse:
    """
    Logout current user.

    Note: With JWT tokens, logout is typically handled client-side by
    removing the token. Server-side logout would require token blacklisting.

    Args:
        current_user: Current user from JWT token

    Returns:
        Success message
    """
    return SuccessResponse(
        message="Logged out successfully",
        data={"user_id": current_user["user_id"]},
    )
