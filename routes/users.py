from fastapi import APIRouter, Depends, HTTPException, status
from database import db_dependency
from security import user_dependency, verify_password, hash_password
from models import Users
from schemas import PasswordChangeRequest



router = APIRouter()





@router.get("/")
async def get_user(db: db_dependency, user: user_dependency):
    return db.query(Users).filter(Users.id == user.get("id")).first()




@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def change_password(db: db_dependency, user: user_dependency, request: PasswordChangeRequest):
    user_model = db.query(Users).filter(Users.username == user.get("username")).first()
    
    if not verify_password(request.password, user_model.hashed_password):
        return "Invalid password"
    user_model.hashed_password = hash_password(request.new_password)
    db.commit()
    return 


