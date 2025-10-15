from fastapi import APIRouter, HTTPException, Depends
from models.machine import MachineCreate, Machine, MachineUpdate, MachineRead
from sqlmodel import Session, select, or_
from database import get_session
from pydantic import EmailStr
from datetime import datetime
from enum import Enum
from typing import List
router = APIRouter(
    prefix="/machine",
    tags=["machines"],
)

class SchemaMethod(str, Enum):
    create = "create"
    update = "update"
    read = "read"

@router.post("/create", response_model=MachineRead)
def create_machine(machine: MachineCreate, session: Session = Depends(get_session)):
    if(machine.enum not in ["active", "no_active"]):
        raise HTTPException(status_code=400, detail="Invalid enum value")
    if(len(machine.name) > 10):
        raise HTTPException(status_code=400, detail="Name exceeds maximum length of 10 characters")
    db_machine = Machine(**machine.model_dump())
    session.add(db_machine)
    session.commit()
    session.refresh(db_machine)
    return db_machine


@router.get("/get", response_model=List[MachineRead])
def get_machine(id: str | None = None,email: EmailStr | None = None,session: Session = Depends(get_session)):
    if id and email:
        items = session.exec(select(Machine).where((Machine.id == id) & (Machine.email == email))).all()
    elif id:
        items = session.exec(select(Machine).where(Machine.id == id)).all()
    elif email:
        items = session.exec(select(Machine).where(Machine.email == email)).all()
    else:
        items = session.exec(select(Machine)).all()

    if not items:
        raise HTTPException(status_code=404, detail="No machines found")

    return items

# @router.get('/get', response_model=List[MachineRead])
# def get_machine(email: EmailStr | None = None, id: int | None = None, session: Session = Depends(get_session)):
#     if not email and not id:
#         statement = select(Machine)
#         results = session.exec(statement)
#         machines = results.all()
#         return machines
    
#     conditions = []
#     if email and not id:
#         conditions.append(Machine.email == email)
#     if id and not email:
#         conditions.append(Machine.id == id)
    
#     if email and id:
#         statement = select(Machine).where(*conditions)
#     else:
#         statement = select(Machine).where(or_(*conditions))

#     results = session.exec(statement)
#     machines = results.all()
    
#     if not machines:
#         raise HTTPException(status_code=404, detail="Machine not found")
    
#     return machines

@router.put('/update', response_model=MachineRead)
def update_machine(machine: MachineUpdate, machine_id: int, session: Session = Depends(get_session)):
    db_machine = session.get(Machine, machine_id)
    if not db_machine:
        raise HTTPException(status_code=404, detail="Machine not found")
        
    for key, value in machine.model_dump(exclude_unset=True).items():
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
    elif method == "update":
        return MachineUpdate.model_json_schema()
    elif method == "read":
        return MachineRead.model_json_schema()
    else:
        raise HTTPException(status_code=400, detail="Wrong method")