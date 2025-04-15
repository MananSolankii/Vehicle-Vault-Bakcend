import csv
import os
import shutil
from io import StringIO

from bson import ObjectId

from config.cloudinary_config import cloudinary
from config.database import carsCollection
from fastapi import File, HTTPException, UploadFile, Query
from fastapi.responses import JSONResponse
from models.CarModel import Car, CarOut

UPLOAD_DIR = "uploads/cars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def getAllCars():
    cars = await carsCollection.find().to_list(None)
    if not cars:
        return JSONResponse(status_code=404, content={"message": "No cars found"})

    car_list = []
    for car in cars:
        car["_id"] = str(car["_id"])
        car["company_id"] = str(car["company_id"]) if "company_id" in car else "Unknown"

        try:
            car_list.append(CarOut(**car))
        except Exception as e:
            print(f"⚠️ Skipping car due to error: {e}")
            continue

    return car_list


async def addCar(car: Car):
    car_data = car.dict()
    car_data["company_id"] = ObjectId(car.company_id)

    newCar = await carsCollection.insert_one(car_data)
    if newCar.inserted_id:
        return JSONResponse(
            status_code=200, content={**car.dict(), "id": str(newCar.inserted_id)}
        )

    raise HTTPException(status_code=500, detail="Car was not added")


async def deleteCarById(id: str):
    try:
        deleteCar = await carsCollection.delete_one({"_id": ObjectId(id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid car ID format")

    if deleteCar.deleted_count == 1:
        return {"message": "Car deleted successfully"}

    raise HTTPException(status_code=404, detail=f"Car with id {id} not found")


async def getCarsByCompany(company_id: str):
    try:
        company_obj_id = ObjectId(company_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid company_id format")

    cars = await carsCollection.find({"company_id": company_obj_id}).to_list(None)

    if not cars:
        return JSONResponse(
            status_code=404, content={"message": "No cars found for this company"}
        )

    for car in cars:
        car["_id"] = str(car["_id"])
        car["company_id"] = str(car["company_id"])

    return [CarOut(**car) for car in cars]


async def uploadCarImage(car_id: str, file: UploadFile = File(...)):
    try:
        car_obj_id = ObjectId(car_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid car ID format")

    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    image_url = f"http://localhost:8000/{file_location}"
    result = await carsCollection.update_one(
        {"_id": car_obj_id}, {"$set": {"image_url": image_url}}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Car not found or image not updated"
        )

    return {"message": "Image uploaded successfully", "image_url": image_url}


async def uploadCarsBulk(file: UploadFile = File(...)):
    contents = await file.read()
    csv_reader = csv.DictReader(StringIO(contents.decode()))

    cars_to_insert = []

    for row in csv_reader:
        try:
            # Handle image URL via Cloudinary
            image = row.get("image_url", "")
            final_image_url = None

            if image:
                try:
                    if image.startswith("http"):
                        final_image_url = image
                    else:
                        final_image_url = f"http://localhost:8000/{image}"
                except Exception as e:
                    print(f"⚠️ Image upload failed for {row['name']}: {e}")
                    final_image_url = None

            car_data = {
                "company_id": ObjectId(row["company_id"]),
                "brand": row["brand"],
                "name": row["name"],
                "model": row["model"],
                "price": float(row["price"]),
                "engine_type": row["engine_type"],
                "cylinders": int(row["cylinders"]),
                "transmission": row["transmission"],
                "fuel_type": row["fuel_type"],
                "mileage_city": float(row["mileage_city"]),
                "mileage_highway": float(row["mileage_highway"]),
                "fuel_tank_capacity": float(row["fuel_tank_capacity"]),
                "length": int(row["length"]),
                "width": int(row["width"]),
                "height": int(row["height"]),
                "wheelbase": int(row["wheelbase"]),
                "ground_clearance": int(row["ground_clearance"]),
                "seating_capacity": int(row["seating_capacity"]),
                "boot_space": int(row["boot_space"]),
                "body_type": row["body_type"],
                "drive_type": row["drive_type"],
                "power_steering": row["power_steering"].lower() == "true",
                "power_windows": row["power_windows"].lower() == "true",
                "air_conditioner": row["air_conditioner"].lower() == "true",
                "automatic_climate_control": row["ACC"].lower() == "true",
                "cruise_control": row["cruise_control"].lower() == "true",
                "sunroof": row["sunroof"].lower() == "true",
                "touch_screen": row["infotainment_system"].lower() == "true",
                "abs": row["ABS"].lower() == "true",
                "airbags": row["airbags"].lower() == "true",
                "parking_sensors": row["parking_sensors"].lower() == "true",
                "rear_camera": row["reverse_camera"].lower() == "true",
                "central_locking": row["central_locking"].lower() == "true",
                "child_safety_lock": row["child_safety_lock"].lower() == "true",
                "bluetooth_connectivity": True,  # optional or default
                "rear_ac_vents": True,  # optional or default
                "usb_ports": 2,  # optional or default
                "speakers": 4,  # optional or default
                "max_power": "N/A",  # optional
                "max_torque": "N/A",  # optional
                "valves_per_cylinder": 4,  # optional
                "engine_displacement": 1200,  # optional
                "image_url": final_image_url,
            }

            cars_to_insert.append(car_data)

        except Exception as e:
            raise HTTPException(status_code=400, detail=f"CSV row parse error: {e}")

    if not cars_to_insert:
        raise HTTPException(status_code=400, detail="CSV file is empty or invalid")

    result = await carsCollection.insert_many(cars_to_insert)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Cars uploaded successfully with Cloudinary images",
            "inserted_ids": [str(_id) for _id in result.inserted_ids],
        },
    )


# 🔍 Exact Match - Used by search bar to redirect to car detail page
async def getCarByName(name: str):
    car = await carsCollection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car["_id"] = str(car["_id"])
    car["company_id"] = str(car["company_id"])
    return CarOut(**car)


# 🔍 Partial Match - Used for autocomplete or search suggestions
async def getCarsByPartialName(query: str):
    cars = await carsCollection.find({"name": {"$regex": query, "$options": "i"}}).to_list(length=10)

    if not cars:
        raise HTTPException(status_code=404, detail="No matching cars found")

    result = []
    for car in cars:
        car["_id"] = str(car["_id"])
        car["company_id"] = str(car["company_id"])
        result.append(CarOut(**car))

    return result
async def getCarById(id: str):
    try:
        car_obj_id = ObjectId(id)
    except:
        raise HTTPException(status_code=400, detail="Invalid car ID format")

    car = await carsCollection.find_one({"_id": car_obj_id})
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car["_id"] = str(car["_id"])
    car["company_id"] = str(car["company_id"])
    return CarOut(**car)