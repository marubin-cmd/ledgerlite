from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Literal
from app.db.dependencies import get_db
from app.models.category import Category
from app.models.transaction import Transaction
from app.schemas.category import CategoryCreate, CategoryResponse


router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.post(
    "",
    response_model= CategoryResponse,
    status_code=status.HTTP_201_CREATED
)

def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    db_category = Category(**category.model_dump())

    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    

    return db_category

@router.get(
    "",
    response_model= list[CategoryResponse]
)

def get_categories(
    category_type: Literal["income", "expense"] | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Category)

    if category_type is not None:

        query = query.filter(Category.category_type == category_type)


    categories = query.all()

    return categories

@router.put(
    "/{category_id}",
    response_model= CategoryResponse,

)

def update_category(
    category_id: int,
    category: CategoryCreate,
    db: Session = Depends(get_db)
):

    db_category = db.query(Category).filter(
        Category.id == category_id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    for key, value in category.model_dump().items():
        setattr(db_category, key, value)


    db.commit()
    db.refresh(db_category)

    return db_category


@router.delete(
    "/{category_id}",
    status_code= status.HTTP_204_NO_CONTENT
)

def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):

    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "Category not found",
        )

    transactions = db.query(Transaction).filter(
        Transaction.category_id == category_id
    ).first()

    if transactions is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete category because transactions are assigned to it"
        )


    db.delete(category)
    db.commit()
    