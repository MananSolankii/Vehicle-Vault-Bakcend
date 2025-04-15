from config.database import rolesCollection
from models.RoleModel import Role, RoleOut
from bson import ObjectId

async def getAllRoles():
    roles =await rolesCollection.find().to_list()
    return [RoleOut(**role) for role in roles]

async def addRole(role:Role):
    result =  await rolesCollection.insert_one(role.dict())
    print(result)
    return{"message":"role inserted successfully.."}

async def deleteRole(roleId:str):
    result = await rolesCollection.delete_one({"_id":ObjectId(roleId)})
    print(result)
    return{"message":"role deleted successfully"}

async def getRoleById(roleId:str):
    result = await rolesCollection.find_one({"_id":ObjectId(roleId)})
    print(result)
    return RoleOut(**result)