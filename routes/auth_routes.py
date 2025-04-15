from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from config.database import userCollection, rolesCollection
from auth.jwt_handler import create_access_token
from passlib.context import CryptContext
from bson import ObjectId

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_EMAILS = ["manan@gmail.com"]  # ⭐️ Admin Emails List


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await userCollection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Credentials")

    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect Password")

    # ⭐️ Fetch Role from rolesCollection
    role = None
    if user.get("role"):
        role = await rolesCollection.find_one({"_id": ObjectId(user["role"])})
        role_name = role["name"].capitalize() if role else "User"
    else:
        role_name = "User"

    # ⭐️ Dynamic Role Assignment Logic
    if user["email"] in ADMIN_EMAILS:
        role_name = "Admin"

    access_token = create_access_token({"sub": str(user["_id"]), "role": role_name})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": role_name,
        "user_id": str(user["_id"]),
        "email": user["email"]
    }
