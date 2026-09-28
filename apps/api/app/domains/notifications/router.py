from fastapi import APIRouter
router = APIRouter()

@router.get("/")
async def list_notifications():
    return []

@router.put("/{id}/read")
async def read_notification(id: str):
    return {"message": "read"}

@router.put("/read-all")
async def read_all():
    return {"message": "all read"}
