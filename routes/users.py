from fastapi import APIRouter, Depends, HTTPException, status
from database import db_dependency
from security import user_dependency, verify_password, hash_password
from models import Users
from schemas import PasswordChangeRequest, PhoneNumberUpdateRequest, PhoneNumberUpdateResponse



router = APIRouter()





@router.get("/")
async def get_user(db: db_dependency, user: user_dependency):
    return db.query(Users).filter(Users.id == user.get("id")).first()




@router.post("/change-password", status_code=status.HTTP_202_ACCEPTED)
async def change_password(db: db_dependency, user: user_dependency, request: PasswordChangeRequest):
    user_model = db.query(Users).filter(Users.username == user.get("username")).first()
    
    if not verify_password(request.password, user_model.hashed_password):
        return "Invalid password"
    user_model.hashed_password = hash_password(request.new_password)
    db.commit()
    return 


@router.put("/phone-number", response_model=PhoneNumberUpdateResponse, status_code=status.HTTP_202_ACCEPTED)
async def update_phone_number(db: db_dependency, user: user_dependency, request: PhoneNumberUpdateRequest):
    user_model = db.query(Users).filter(Users.username == user.get('username')).first()
    if not (user_model.phone_number == request.old_number):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old Password not match")
    
    user_model.phone_number = request.new_number
    
    db.commit()
    return {"new_number" : user_model.phone_number}
