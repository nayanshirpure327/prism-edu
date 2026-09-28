from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_institutions():
    return []

@router.get("/{slug}")
async def get_institution(slug: str):
    return {"slug": slug}

@router.post("/compare")
async def compare_institutions():
    return []

@router.get("/{slug}/programs")
async def get_programs(slug: str):
    return []

@router.post("/save/{id}")
async def save_institution(id: str):
    return {"message": "saved"}

@router.get("/saved")
async def saved_institutions():
    return []
