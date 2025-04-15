from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import get_current_user

security = HTTPBearer()

async def get_user_payload(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return await get_current_user(token)

async def admin_required_bearer(user=Depends(get_user_payload)):
    if user.get("role", {}).get("name") != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")

async def user_required_bearer(user=Depends(get_user_payload)):
    if user.get("role", {}).get("name") != "User":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User access required")
