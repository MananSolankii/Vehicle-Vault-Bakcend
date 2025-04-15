from controllers.RoleController import addRole, deleteRole, getAllRoles, getRoleById
from fastapi import APIRouter
from models.RoleModel import Role

router = APIRouter()


@router.get("/roles/")
async def get_roles():
    return await getAllRoles()


@router.post("/role/")
async def post_role(role: Role):
    return await addRole(role)


@router.delete("/role/{roleId}")
async def delete_role(roleId: str):
    return await deleteRole(roleId)


@router.get("/roles/{roleId}")
async def getroleById(roleId: str):
    return await getRoleById(roleId)
