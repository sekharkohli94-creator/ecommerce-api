from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_admin
from app.models import User
from app.schemas import UserResponse


router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)


# =========================
# GET ALL USERS
# =========================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_all_users(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    return db.query(User).all()


# =========================
# GET ONE USER
# =========================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# =========================
# MAKE USER ADMIN
# =========================

@router.put(
    "/{user_id}/admin",
    response_model=UserResponse
)
def make_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.is_admin = True

    db.commit()
    db.refresh(user)

    return user


# =========================
# REMOVE ADMIN
# =========================

@router.put(
    "/{user_id}/remove-admin",
    response_model=UserResponse
)
def remove_admin(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Prevent removing your own admin access
    if user.id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot remove your own admin access"
        )

    user.is_admin = False

    db.commit()
    db.refresh(user)

    return user