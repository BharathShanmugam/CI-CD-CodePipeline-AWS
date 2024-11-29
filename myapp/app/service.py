from sqlalchemy.orm import Session
from . import model, schema

def create_user(db: Session, user: schema.UserCreate):
    db_user = model.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(model.User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(model.User).filter(model.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
