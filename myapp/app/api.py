from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schema, service, db

router = APIRouter()

@router.post("/users/", response_model=schema.UserResponse)
def create_user(user: schema.UserCreate, db: Session = Depends(db.get_db)):
    return service.create_user(db, user)

@router.get("/users/", response_model=list[schema.UserResponse])
def read_users(db: Session = Depends(db.get_db)):
    return service.get_users(db)

@router.get("/users/{user_id}", response_model=schema.UserResponse)
def read_user(user_id: int, db: Session = Depends(db.get_db)):
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(db.get_db)):
    if not service.delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
