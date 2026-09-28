from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_profile():
    return {"profile": {}}

@router.put("/")
async def update_profile():
    return {"message": "updated"}

@router.post("/wizard/step/{step}")
async def submit_wizard(step: int):
    return {"message": f"step {step} submitted"}

@router.get("/wizard/step/{step}")
async def get_wizard(step: int):
    return {"step": step, "data": {}}

@router.get("/academic-records")
async def list_academic_records():
    return []

@router.post("/academic-records")
async def add_academic_record():
    return {"message": "added"}

@router.get("/completion")
async def get_completion():
    return {"completion_pct": 100}
