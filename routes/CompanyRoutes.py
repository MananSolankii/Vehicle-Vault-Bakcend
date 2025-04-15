from auth.jwt_bearer import admin_required_bearer
from controllers import CompayController
from fastapi import APIRouter, Depends, File, UploadFile
from models.CompanyModel import Company

router = APIRouter()


@router.get("/companies")
async def getAllCompanies():
    return await CompayController.getAllCompanies()


@router.get("/company/{id}")
async def getCompanyById(id: str):
    return await CompayController.getCompanyById(id)


@router.post("/company", dependencies=[Depends(admin_required_bearer)])
async def addCompany(company: Company):
    return await CompayController.addCompany(company)


@router.post("/companies/bulk", dependencies=[Depends(admin_required_bearer)])
async def addCompaniesBulk(companies: list[Company]):
    return await CompayController.addCompaniesInBulk(companies)


@router.delete("/company/{id}")
async def deleteCompanyById(id: str):
    return await CompayController.deleteCompanyById(id)


@router.post("/company/upload-csv")
async def upload_companies_csv(file: UploadFile = File(...)):
    return await CompayController.upload_companies_csv(file)
