from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from sqlite3 import IntegrityError
import traceback
from app import crud, schemas
from app.core.logging_config import setup_logger
from app.database import get_db
from app.auth.dependencies import get_current_active_user
from app.models import User

router = APIRouter()
logger = setup_logger()

def check_dept_permission(db: Session, user: User, dept_id: UUID, required_permission: str = "view"):
    """
    Helper function to check department permissions
    required_permission: "view", "edit", or "Admin"
    """
    dept = crud.get_department(db, dept_id)
    if not dept:
        return False
    
    # SuperAdmins can do anything
    if any(role.role.name == "SuperAdmin" for role in user.user_roles):
        return True
    
    # Check if user belongs to the dept's parent product
    if user.prod_id != dept.parent_prod_id:
        return False
    
    # product SuperAdmins have full access to their org's depts
    if any(role.role.name == "Admin" for role in user.user_roles):
        return True
    
    # dept SuperAdmins have full access to their own dept
    if any(role.role.name == "ContentManager" for role in user.user_roles):
        return True
    
    # Regular users can only view if they belong to the dept
    if required_permission == "view" and user.dept_id == dept_id:
        return True
    
    return False

@router.post("/", response_model=schemas.DepartmentInDB, status_code=status.HTTP_201_CREATED)
def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    """
    Create a new department (product Admin or SuperAdmin only)
    Automatically sets parent_prod_id to current user's product unless SuperAdmin specifies
    """
    # Check if user has product Admin privileges
    if not (any(role.role.name == "SuperAdmin" for role in current_user.user_roles) or 
            any(role.role.name == "Admin" for role in current_user.user_roles) or any(role.role.name == "ContentManager" for role in current_user.user_roles)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create departments"
        )

    # Use current user's org as parent (unless SuperAdmin specifying different org)
    parent_prod_id = current_user.prod_id
    if any(role.role.name == "SuperAdmin" for role in current_user.user_roles) and department.parent_prod_id:
        parent_prod_id = department.parent_prod_id

    # Check if parent product exists
    logger.info(f"....{parent_prod_id}")
    parent_org = crud.get_product(db, parent_prod_id)
    logger.info(f"parent-prg{parent_org}")
    if not parent_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent product not found"
        )

    try:
        # Create the department
        db_dept = crud.create_department(
            db=db,
            department=department,
            parent_prod_id=parent_org.prod_id
        )
        
        # Create the Admin user if credentials provided
        if hasattr(department, 'SuperAdmin_email'):
            # Create user with ContentManager role
            SuperAdmin_data = schemas.UserCreate(
                email=department.SuperAdmin_email,
                first_name=department.SuperAdmin_first_name,
                last_name=department.SuperAdmin_last_name,
                password="sub12378",  # Should be provided in the request
                prod_id=parent_prod_id,
                dept_id=db_dept.dept_id,
                is_active=True,
                folder=department.folder
            )
            # SuperAdmin_user = crud.create_user(db=db, user=SuperAdmin_data, role_names=["ContentManager"])
        
        return db_dept
        
    except IntegrityError:
        print("Exception:", traceback.format_exc())
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="department creation failed (possible duplicate name)"
        )

@router.get("/parent/{parent_prod_id}", response_model=List[schemas.DepartmentInDB])
def read_departments_by_parent(
    parent_prod_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    """
    Retrieve departments by parent ID
    """
    # Check if parent product exists
    parent_org = crud.get_product(db, parent_prod_id)
    if not parent_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parent product not found"
        )
    
    # Check permissions
    if not (any(role.role.name == "SuperAdmin" for role in current_user.user_roles) or
            current_user.prod_id == parent_prod_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view these departments"
        )
    
    return crud.get_departments_by_parent(
        db, parent_prod_id=parent_prod_id, skip=skip, limit=limit
    )

@router.get("/{dept_id}", response_model=schemas.DepartmentInDB)
def read_department(
    dept_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    """
    Get department by ID
    """
    dept = crud.get_department(db, dept_id=dept_id)
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="department not found"
        )
    
    # Check permissions using helper function
    if not check_dept_permission(db, current_user, dept_id, "view"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this department"
        )
    
    return dept

@router.put("/{dept_id}", response_model=schemas.DepartmentInDB)
def update_department(
    dept_id: UUID,
    department: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    """
    Update a department
    """
    db_dept = crud.get_department(db, dept_id=dept_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="department not found"
        )
    
    # Check permissions using helper function
    if not check_dept_permission(db, current_user, dept_id, "edit"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this department"
        )
    
    return crud.update_department(
        db=db, 
        dept_id=dept_id, 
        department=department
    )

@router.delete("/{dept_id}", response_model=schemas.DepartmentInDB)
def delete_department(
    dept_id: UUID,
    db: Session = Depends(get_db),
    current_user: schemas.UserInDB = Depends(get_current_active_user)
):
    """
    Delete a department (product Admin or SuperAdmin only)
    """
    db_dept = crud.get_department(db, dept_id=dept_id)
    if not db_dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="department not found"
        )
    
    # Check permissions
    if not (any(role.role.name == "SuperAdmin" for role in current_user.user_roles) or
            (current_user.prod_id == db_dept.parent_prod_id and 
             any(role.role.name == "Admin" for role in current_user.user_roles))):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this department"
        )
    
    return crud.delete_department(db=db, dept_id=dept_id)
