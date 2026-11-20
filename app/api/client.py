from fastapi import APIRouter, Depends, status, HTTPException
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse
from app.db.dependencies import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post(
    "",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED
)

def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):

    if client.email is not None:

        existing_email = db.query(Client).filter(
            Client.email == client.email
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A client with this email already exists"
            )

    db_client = Client(**client.model_dump())

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client


@router.get(
    "",
    response_model=list[ClientResponse]
)

def get_clients(
    name: str | None = None,
    client_id: int | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(Client)

    if client_id is not None:

        query = query.filter(Client.id == client_id)

    if name:
        query = query.filter(Client.name.ilike(f"%{name.strip()}%"))

    clients = query.all()

    return clients



@router.get(
    "/{client_id}",
    response_model=ClientResponse
)
def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    db_client = db.get(Client, client_id)

    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    return db_client



@router.put(
    "/{client_id}",
    response_model=ClientResponse
)

def update_client(
    client_id: int,
    client: ClientCreate,
    db: Session = Depends(get_db)
):

    db_client = db.get(Client, client_id)

    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    if client.email is not None:

        existing_email = db.query(Client).filter(
            Client.email == client.email,
            Client.id != client_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A client with this email already exists"
            )

    for key, value in client.model_dump().items():
        setattr(db_client, key, value)


    db.commit()
    db.refresh(db_client)

    return db_client

@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT
)

def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):

    db_client = db.get(Client, client_id)

    if db_client is None:
            raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )

    db.delete(db_client)
    db.commit()
