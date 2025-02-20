from fastapi import Depends,Request
from fastapi import APIRouter
from slowapi.util import get_remote_address
from app.models.basemodel import *
from app.utils.utils import *
from app.db.database import *
from app.main import limiter

router = APIRouter(tags=["BasicAuth"])

#secure-data-view endpoint with the rate limit 5 calls per minutes.
#Depends on authenticate_user_detail function to validate crendentials.
#Can be accessed by any user.
@router.get("/secure-data-view")
@limiter.limit("5/minute")
async def get_secure_data_view(request: Request, user: dict = Depends(authenticate_user_detail)):
    ip = get_remote_address(request)
    print("Request received from IP: %s"%(ip))
    return {"message": f"Hello, {user['username']}! You have accessed a protected route"}

#secure-data-admin endpoint with the rate limit 5 calls per minutes.
#Depends on authenticate_user_detail and requre_role_ba functions to validate crendentials and authrorization.
#Can be accessed by only admin user.
@router.get("/secure-data-admin")
@limiter.limit("5/minute")
async def get_secure_data_admin(request: Request, user: dict = Depends(authenticate_user_detail), role: str = Depends(require_role_ba("admin"))):
    return {"message": f"Hello, {user['username']}! You have accessed a protected route. {role}"}