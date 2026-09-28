from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_assessments():
    return []

@router.get("/{id}")
async def get_assessment(id: str):
    return {"id": id}

@router.post("/{id}/start")
async def start_assessment(id: str):
    return {"message": "started"}

@router.post("/attempts/{attempt_id}/submit")
async def submit_assessment(attempt_id: str):
    return {"message": "submitted"}

@router.get("/attempts/{attempt_id}/result")
async def assessment_result(attempt_id: str):
    return {"result": {}}

@router.get("/results")
async def list_results():
    return []
