from models.CompanyModel import Company, CompanyOut
from config.database import companyCollection
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import UploadFile, HTTPException
import csv
from io import StringIO


async def getAllCompanies():
    companies = await companyCollection.find().to_list(None)
    if not companies:
        return JSONResponse(status_code=404, content={"message": "No companies found"})

    for company in companies:
        company["_id"] = str(company["_id"])

    return [CompanyOut(**company) for company in companies]


async def getCompanyById(id: str):
    company = await companyCollection.find_one({"_id": ObjectId(id)})

    if not company:
        return JSONResponse(status_code=404, content={"message": "Company not found"})

    company["_id"] = str(company["_id"]) if "_id" in company else None

    return JSONResponse(status_code=200, content=CompanyOut(**company).model_dump())


async def addCompany(company: Company):
    newCompany = await companyCollection.insert_one(company.dict())
    if newCompany.inserted_id:
        return JSONResponse(status_code=200, content=company.dict())
    raise HTTPException(status_code=500, detail="Company not added.")


async def deleteCompanyById(id: str):
    deleteCompany = await companyCollection.delete_one({"_id": ObjectId(id)})
    if deleteCompany.deleted_count == 1:
        return {"message": "Company deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Company with id {id} not found")


async def addCompaniesInBulk(companies: list[Company]):
    company_data = [company.dict() for company in companies]
    result = await companyCollection.insert_many(company_data)

    if result.inserted_ids:
        return JSONResponse(status_code=200, content={"message": "Companies added successfully", "inserted_ids": [str(_id) for _id in result.inserted_ids]})

    raise HTTPException(status_code=500, detail="Companies not added.")

async def upload_companies_csv(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    decoded = contents.decode('utf-8')
    csv_reader = csv.DictReader(StringIO(decoded))

    companies = []
    for row in csv_reader:
        name = row.get("name")
        if name:
            companies.append({"name": name.strip()})

    if not companies:
        raise HTTPException(status_code=400, detail="No valid company data found")

    result = await companyCollection.insert_many(companies)
    return {"message": "Companies added", "inserted_ids": [str(_id) for _id in result.inserted_ids]}

