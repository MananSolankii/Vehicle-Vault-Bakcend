from fastapi import FastAPI
from routes.RoleRoutes import router as role_router
from routes.CarRoutes import router as car_router
from fastapi.middleware.cors import CORSMiddleware
from routes.UserRoutes import router as User_router
from routes.CompanyRoutes import router as Company_router
from routes.auth_routes import router as auth_router  # ✅ Added Auth Router
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",  # ⭐️ Add this
    "http://127.0.0.1:5174"   # ⭐️ Add this
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_router)
app.include_router(car_router)
app.include_router(User_router)
app.include_router(Company_router)
app.include_router(auth_router)  # ✅ Include Auth Routes


@app.get("/")
def home():
    return {"message": "CORS enabled successfully!"}