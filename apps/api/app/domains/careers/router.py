from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_careers():
    return []

@router.get("/{slug}")
async def get_career(slug: str):
    return {"slug": slug}

@router.get("/{slug}/related")
async def get_related(slug: str):
    return []

@router.get("/industries")
async def list_industries():
    return []

@router.get("/skills")
async def list_skills():
    return []

@router.post("/save/{id}")
async def save_career(id: str):
    return {"message": "saved"}

@router.delete("/save/{id}")
async def unsave_career(id: str):
    return {"message": "unsaved"}

@router.get("/saved")
async def saved_careers():
    return []
