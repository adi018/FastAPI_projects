from fastapi import FastAPI

app = FastAPI()

@app.get("/auth/")
async def get_user():   
    """
    Endpoint to get user information.
    This endpoint retrieves user information.
    """
    return {"user": "authenticated_user"}