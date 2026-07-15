from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def memory_status():
    return {
        "module": "memory",
        "status": "ready"
    }