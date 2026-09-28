from fastapi import APIRouter
router = APIRouter()

@router.post("/generate")
async def generate():
    return {"message": "generating"}

@router.get("/")
async def list_pathways():
    return []

@router.get("/{id}")
async def pathway_details(id: str):
    return {"id": id}

@router.put("/{id}/save")
async def save_pathway(id: str):
    return {"message": "saved"}

@router.delete("/{id}")
async def archive_pathway(id: str):
    return {"message": "archived"}

@router.get("/{id}/cost-breakdown")
async def cost_breakdown(id: str):
    return {"total_cost": 0}
