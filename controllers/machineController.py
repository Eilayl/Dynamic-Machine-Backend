from fastapi import APIRouter, HTTPException, Depends
from models.machine import Machine
from sqlmodel import Session, select
from database import get_session

router = APIRouter(
    prefix="/machines",
    tags=["machines"],
)

@router.post("/create")
def create_machine(machine: Machine, session: Session = Depends(get_session)):
    session.add(machine)
    session.commit()
    session.refresh(machine)
    return machine

@router.get("/all")
def get_all_machines(session: Session = Depends(get_session)):
    machines = session.exec(select(Machine)).all()
    print(f"Found {len(machines)} machines")
    return machines


@router.post("/update/{machine_id}")
def machine_update():
    if not machine_id:
        raise HTTPException(status_code=400, detail="Machine ID is required")
    machine = session.get(Machine, machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    for key, value in machine.dict().items():
        setattr(machine, key, value)
    session.add(machine)
    session.commit()
    session.refresh(machine)
    return machine

