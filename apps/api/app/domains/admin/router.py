from fastapi import APIRouter
router = APIRouter()

@router.get("/careers")
async def list_admin_careers(): return []
@router.post("/careers")
async def create_admin_career(): return {"status": "ok"}
@router.put("/careers/{id}")
async def update_admin_career(id: str): return {"status": "ok"}
@router.delete("/careers/{id}")
async def delete_admin_career(id: str): return {"status": "ok"}

@router.get("/institutions")
async def list_admin_institutions(): return []
@router.post("/institutions")
async def create_admin_institution(): return {"status": "ok"}

@router.get("/scholarships")
async def list_admin_scholarships(): return []
@router.post("/scholarships")
async def create_admin_scholarship(): return {"status": "ok"}

@router.get("/loans")
async def list_admin_loans(): return []
@router.post("/loans")
async def create_admin_loan(): return {"status": "ok"}

@router.get("/audit-logs")
async def list_admin_audit_logs(): return []

@router.get("/users")
async def list_admin_users(): return []
@router.put("/users/{id}/role")
async def update_user_role(id: str): return {"status": "ok"}
