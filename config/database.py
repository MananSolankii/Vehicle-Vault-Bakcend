from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://localhost:27017"
DATABASE_NAME = "Vehice_vault"
client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]
rolesCollection = db["roles"]
carsCollection = db["cars"]
userCollection = db["users"]
companyCollection = db["company"]
