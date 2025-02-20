from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Request
from fastapi import APIRouter
from slowapi.util import get_remote_address
from app.models.basemodel import *
from app.utils.utils import *
from app.db.database import *
from app.main import limiter

router = APIRouter(tags=["JWTAuth"])

#login endpoint is to generate token after validating credentials.
#rate limit - 5 calls per minute.
@router.post("/login", response_model=Token, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

#secure-data--jwt-view endpoint with the rate limit 5 calls per minutes.
#Depends on get_current_user function to validate crendentials.
#Can be accessed by any user.
@router.get("/secure-data-jwt-view")
@limiter.limit("5/minute")
async def secure_data_jwt_view(request: Request, current_user: User = Depends(get_current_user)):
    return {"Username": current_user}

#secure-data--jwt-admin endpoint with the rate limit 5 calls per minutes.
#Depends on get_current_user and require_role_jwt functions to validate crendentials and authorization.
#Can be accessed by only admin user.
@router.get("/secure-data-jwt-admin")
@limiter.limit("5/minute")
async def secure_data_jwt_admin(request: Request, current_user: User = Depends(get_current_user), role: str = Depends(require_role_jwt("admin"))):
    return {"Username": current_user}