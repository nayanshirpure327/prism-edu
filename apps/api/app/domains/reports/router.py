from fastapi import APIRouter
router = APIRouter()

@router.post("/generate")
async def generate_report():
    return {"message": "generating"}

@router.get("/{id}/status")
async def report_status(id: str):
    return {"status": "ready"}

@router.get("/{id}/download")
async def download_report(id: str):
    return {"url": "file_url"}
