from fastapi import APIRouter, Depends, status
from app.api.v1.schemas.user import UserResponse, UserCreate, UserUpdate
from app.api.v1.services.user import create_user, get_all_users, get_user, edit_user, remove_user
from app.api.v1.models.user import User
from app.api.core.security import get_current_user, admin_only
from app.api.db.database import get_db
from sqlalchemy.orm import Session
from typing import List


user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@user_router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    return get_all_users(skip=skip, limit=limit, db=db, current_user=current_user)

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    return get_user(user_id=user_id, db=db, current_user=current_user)

@user_router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return edit_user(user_id=user_id, user=user, db=db, current_user=current_user)

@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return remove_user(user_id=user_id, db=db, current_user=current_user)