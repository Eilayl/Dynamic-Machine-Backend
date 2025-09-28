from fastapi import APIRouter, HTTPException, Depends
from requests import session
from models.machine import MachineCreate, Machine, MachineUpdate
from sqlmodel import Session, select
from database import get_session
from pydantic import EmailStr
from datetime import datetime
from enum import Enum



router = APIRouter(
    prefix="/machine",
    tags=["machines"],
)

class SchemaMethod(str, Enum):
    create = "create"
    update = "update"

@router.post("/create")
def create_machine(machine: MachineCreate, session: Session = Depends(get_session)):
    db_machine = Machine(**machine.dict())
    session.add(db_machine)
    session.commit()
    session.refresh(db_machine)
    return db_machine

@router.get('/get')
def get_machine(email: EmailStr, id: int, session: Session = Depends(get_session)):
    statement = select(Machine).where(Machine.email == email, Machine.id == id)
    results = session.exec(statement)
    machine = results.first()
    if not machine:
        return HTTPException(status_code=404, detail="Machine not found")
    return machine


@router.put('/update')
def update_machine(machine: MachineUpdate, machine_id: int, session: Session = Depends(get_session)):
    db_machine = session.get(Machine, machine_id)
    if not db_machine:
        return HTTPException(status_code=404, detail="Machine not found")
    for key, value in machine.dict(exclude_unset=True).items():
        setattr(db_machine, key, value)
    
    db_machine.updated_at = datetime.utcnow()
    session.add(db_machine)
    session.commit()
    session.refresh(db_machine)
    return db_machine

@router.get('/schema/{method}')
def get_schema(method: SchemaMethod):
    if method == "create":
        return MachineCreate.model_json_schema()
    if method == "update":
        return MachineUpdate.model_json_schema()
    else:
        return HTTPException(status_code=400, detail="Wrong method")