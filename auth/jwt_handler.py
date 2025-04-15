from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from config.database import userCollection, rolesCollection
from bson import ObjectId

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await userCollection.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception

    role = await rolesCollection.find_one({"_id": user.get("role")})
    user["role"] = {"name": role["name"]} if role else None

    return user

async def admin_required(user=Depends(get_current_user)):
    if user.get("role", {}).get("name") != "Admin":
        raise HTTPException(status_code=403, detail="Admin access required")

async def user_required(user=Depends(get_current_user)):
    if user.get("role", {}).get("name") != "User":
        raise HTTPException(status_code=403, detail="User access required")