from fastapi import APIRouter, HTTPException, status, Depends
from database import db_dependency
from schemas import UsersCreateRequest, UserCreateResponse, Token
from models import Users
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from security import hash_password, verify_password, create_access_token
from datetime import timedelta


router = APIRouter()


@router.post("/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
async def signup(db: db_dependency, request: UsersCreateRequest):
    existing_user = db.query(Users).filter(Users.username == request.username).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="User already exists"
            )
        
    try:
        user_model = Users(
            username = request.username,
            email = request.email,
            hashed_password = hash_password(request.password),
            first_name = request.first_name,
            last_name = request.last_name,
            role = request.role
        )
        
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return user_model
    
    except Exception as e:
        print(f"DB error {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
            )


@router.post("/token", response_model=Token, status_code=status.HTTP_202_ACCEPTED)
async def login_for_token(db: db_dependency, form_data : Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_model = db.query(Users).filter(Users.username == form_data.username).first()
    
    if not user_model or not verify_password(form_data.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
    
    token = create_access_token(username=user_model.username, user_id=user_model.id, user_role=user_model.role, expires_delta=timedelta(minutes=20))
    
    return {"access_token" : token, "token_type" : "Bearer"}

    


@router.post("/me")
async def get_user_details(db: db_dependency):
    pass