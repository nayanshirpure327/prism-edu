from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def search_scholarships():
    return []

@router.get("/{slug}")
async def get_scholarship(slug: str):
    return {"slug": slug}

@router.post("/match")
async def match_scholarships():
    return []

@router.post("/save/{id}")
async def save_scholarship(id: str):
    return {"message": "saved"}

@router.get("/saved")
async def saved_scholarships():
    return []
