from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.dependencies import get_db
from app.models.category import Category
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
    category_type: str | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Category)

    if category_type:

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
    