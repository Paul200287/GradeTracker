from collections.abc import Generator
from typing import Annotated

from sqlalchemy.orm import Session

import jwt
from fastapi import Depends, HTTPException, status, Path
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.database.session import engine
from app.core import security
from app.core.config import settings

from app.schemas.token import TokenData
from app.schemas.user import User
from app.crud.user import get_user_by_email

from app.models.role import Role

# Database Session
def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.

    This function is a generator that yields a SQLAlchemy session object.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]

# Security
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)

TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
    """
    Retrieve the current user based on the provided session and token.

    Args:
        session (SessionDep): The database session dependency.
        token (TokenDep): The JWT token dependency.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If the token is invalid, credentials cannot be validated,
                       the user is not found, or the user is inactive.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        token_data = TokenData(username=username)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = get_user_by_email(db=session, email=token_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.updated_at: # change to deleted_at
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    """
    Verify if the current user is a superuser.

    Args:
        current_user (CurrentUser): The user object to be checked.

    Returns:
        User: The current user if they are a superuser.

    Raises:
        HTTPException: If the current user is not a superuser, an HTTP 403 Forbidden exception is raised.
    """
    if current_user.role != "Superuser":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough privileges"
        )
    return current_user

def require_role(required_role: Role):
    """
    Returns a FastAPI dependency that enforces role-based access control.
    """
    def role_checker(current_user: CurrentUser):
        role_hierarchy = {
            Role.SUPERUSER: 3,
            Role.RACECONTROL: 2,
            Role.RACINGTEAM: 1,
            Role.STARTLINEJUDGE: 0
        }

        if role_hierarchy[current_user.role] < role_hierarchy[required_role]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required permissions ({required_role.value} or higher)."
            )
        return current_user

    return Depends(role_checker)

def require_team_membership(team_id: int = Path(..., description="Team ID from the request path")):
    """
    Dependency to check if a RACINGTEAM user is accessing their own team.
    """
    def membership_dependency(current_user: CurrentUser):
        # Superusers and RaceControl can access all teams
        if current_user.role in {Role.SUPERUSER, Role.RACECONTROL}:
            return current_user  # No restriction needed

        # RACINGTEAM users can only access their own team
        if current_user.role == Role.RACINGTEAM:
            if current_user.team_id != team_id:
                print(team_id)
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this team."
                )
            else:
                return current_user

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this team."
        )

    return Depends(membership_dependency)
