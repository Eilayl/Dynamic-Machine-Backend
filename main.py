from controllers.machineController import router as machine_router
from fastapi import FastAPI
import database 

app = FastAPI()

app.include_router(machine_router)