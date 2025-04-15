from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from config.database import rolesCollection, userCollection
from models.UserModel import User, UserLogin, UserOut
from passlib.context import CryptContext
from auth.jwt_handler import create_access_token

admin_emails = ["admin@gmail.com", "manan@gmail.com"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def getAllUsers():
    users = await userCollection.find().to_list(None)
    if not users:
        return JSONResponse(status_code=404, content={"detail": "No users found"})

    for user in users:
        role = await rolesCollection.find_one({"_id": user.get("role")})
        user["role"] = {"name": role["name"]} if role else None

    return [UserOut(**user) for user in users]

async def addUser(user: User):
    existing_user = await userCollection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists with this email")

    role_name = "Admin" if user.email in admin_emails else "User"
    role = await rolesCollection.find_one({"name": role_name})

    if not role:
        raise HTTPException(status_code=500, detail=f"{role_name} role not found")

    hashed_password = pwd_context.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password
    user_data["role"] = ObjectId(role["_id"])

    result = await userCollection.insert_one(user_data)
    if result.inserted_id:
        return {"message": "User registered successfully"}

    raise HTTPException(status_code=500, detail="User could not be registered")

async def deleteUserById(id: str):
    user = await userCollection.delete_one({"_id": ObjectId(id)})
    if user.deleted_count == 1:
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

async def user_login(user_login: UserLogin):
    user = await userCollection.find_one({"email": user_login.email})

    if not user or not pwd_context.verify(user_login.password, user.get("password")):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    role = await rolesCollection.find_one({"_id": user.get("role")})
    user["role"] = {"name": role["name"]} if role else None

    token_data = {"user_id": str(user["_id"])}
    token = create_access_token(token_data)

    return JSONResponse(status_code=200, content={
        "message": "Login successful",
        "token": token,
        "role": user.get("role", {}).get("name", "User")
    })