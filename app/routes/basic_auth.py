from fastapi import Depends,Request
from fastapi import APIRouter
from slowapi.util import get_remote_address
from app.models.basemodel import *
from app.utils.utils import *
from app.db.database import *
from app.main import limiter

router = APIRouter(tags=["BasicAuth"])

@router.get("/secure-data-view")
@limiter.limit("5/minute")
async def get_secure_data(request: Request, user: dict = Depends(authenticate_user_detail)):
    ip = get_remote_address(request)
    print("Request received from IP: %s"%(ip))
    return {"message": f"Hello, {user['username']}! You have accessed a protected route"}

@router.get("/secure-data-admin")
@limiter.limit("5/minute")
async def get_secure_data(request: Request, user: dict = Depends(authenticate_user_detail), role: str = Depends(require_role_ba("admin"))):
    return {"message": f"Hello, {user['username']}! You have accessed a protected route. {role}"}