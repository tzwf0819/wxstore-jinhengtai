from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User # Assuming you have a User model

# This is a placeholder. In a real app, you would have a more secure way to get the user, e.g., from a JWT token.
api_key_header = APIKeyHeader(name="X-User-Id", auto_error=False)

def get_current_user(api_key: str = Security(api_key_header), db: Session = Depends(get_db)) -> User:
    if not api_key:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_id = int(api_key)
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
