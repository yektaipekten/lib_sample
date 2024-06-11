from fastapi import APIRouter

router = APIRouter()


@router.get("/availability")
async def check_availability() -> bool:

    available = True
    return available
