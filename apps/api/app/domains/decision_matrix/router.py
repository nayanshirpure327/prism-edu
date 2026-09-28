from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def get_matrix():
    return {"weights": {}}

@router.post("/")
async def create_matrix():
    return {"message": "created"}

@router.get("/{id}")
async def get_matrix_result(id: str):
    return {"id": id}

@router.put("/{id}/weights")
async def update_weights(id: str):
    return {"message": "updated"}
