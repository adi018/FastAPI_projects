from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/")
async def get_user():   
    """
    Endpoint to get user information.
    This endpoint retrieves user information.
    """
    return {"user": "authenticated_user"}