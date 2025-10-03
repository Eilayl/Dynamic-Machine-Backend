import os
from controllers.machineController import router as machine_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import database 

app = FastAPI()

# Get frontend URL from environment variable and normalize it
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173").strip()

ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://localhost:3000",
]

print("Allowed origins:", ALLOWED_ORIGINS)  # Debug log

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(machine_router)
