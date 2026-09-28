from fastapi import APIRouter
router = APIRouter()

@router.post("/")
async def create_scenario():
    return {"message": "created"}

@router.get("/")
async def list_scenarios():
    return []

@router.get("/{id}")
async def get_scenario(id: str):
    return {"id": id}

@router.post("/{id}/clone")
async def clone_scenario(id: str):
    return {"message": "cloned"}

@router.put("/{id}")
async def update_scenario(id: str):
    return {"message": "updated"}

@router.delete("/{id}")
async def delete_scenario(id: str):
    return {"message": "deleted"}

@router.post("/compare")
async def compare_scenarios():
    return []
