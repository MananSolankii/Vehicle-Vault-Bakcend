from auth.jwt_bearer import admin_required_bearer
from controllers import CarController
from fastapi import APIRouter, Depends, File, UploadFile
from models.CarModel import Car

router = APIRouter()


@router.get("/cars")
async def getAllCars():
    return await CarController.getAllCars()


@router.get("/car/{id}")
async def getCarById(id: str):
    return await CarController.getCarById(id)


@router.get("/cars/company/{company_id}")
async def getCarsByCompany(company_id: str):
    return await CarController.getCarsByCompany(company_id)


@router.post("/car")
async def addCar(car: Car):
    return await CarController.addCar(car)


@router.post("/car/upload-image/{car_id}")
async def uploadCarImage(car_id: str, file: UploadFile = File(...)):
    return await CarController.uploadCarImage(car_id, file)


@router.delete("/car/{id}")
async def deleteCarById(id: str):
    return await CarController.deleteCarById(id)


# ✅ Bulk car upload using CSV
@router.post("/cars/bulk")
async def uploadCarsBulk(file: UploadFile = File(...)):
    return await CarController.uploadCarsBulk(file)

@router.get("/car-by-name/{name}")
async def getCarByName(name: str):
    return await CarController.getCarByName(name)


@router.get("/cars/search/{query}")
async def getCarsByPartialName(query: str):
    return await CarController.getCarsByPartialName(query)
