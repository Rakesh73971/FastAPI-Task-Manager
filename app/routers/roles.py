from fastapi import Depends, HTTPException, status, APIRouter
from ..models import User
from ..oauth2 import get_current_user

router = APIRouter()

def role_required(allowed_roles: tuple):
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission"
            )
        return current_user
    return checker


@router.get('/admin/dashboard')
def admin_profile(current_user: User = Depends(role_required(('admin',)))):
    return {"message": "Welcome Admin"}


@router.get('/profile')
def user_profile(current_user: User = Depends(role_required(('user', 'admin')))):
    return {"message": f"Hello welcome {current_user.role}"}
