# workflow API

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def workflow_health():
    return {"status": "workflow router is ready"}