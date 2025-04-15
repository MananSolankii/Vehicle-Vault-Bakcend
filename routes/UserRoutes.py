from auth.jwt_bearer import admin_required_bearer
from controllers import UserController
from fastapi import APIRouter, Depends
from models.UserModel import User, UserLogin

router = APIRouter()


@router.get("/users")
async def get_all_users():
    return await UserController.getAllUsers()


# @router.get("/user/{id}", dependencies=[Depends(admin_required_bearer)])
# async def get_user_by_id(id: str):
#     return await UserController.getUserById(id)


@router.post("/user")
async def signup_user(user: User):
    return await UserController.addUser(user)


@router.post("/user/login")
async def login_user(user: UserLogin):
    return await UserController.user_login(user)


@router.delete("/user/{id}", dependencies=[Depends(admin_required_bearer)])
async def delete_user_by_id(id: str):
    return await UserController.deleteUserById(id)
