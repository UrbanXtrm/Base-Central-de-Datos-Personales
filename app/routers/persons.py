"""Rutas para gestionar personas."""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from .. import models
from ..crud import create, delete, get_or_404, list_all, update
from ..database import engine

router = APIRouter(prefix="/persons", tags=["persons"])


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@router.get("/", response_model=list[models.PersonRead])
def get_persons(session: Session = Depends(get_session)):
    return list_all(session, models.Person)


@router.post("/", response_model=models.PersonRead, status_code=201)
def create_person(payload: models.PersonCreate, session: Session = Depends(get_session)):
    person = models.Person.model_validate(payload.model_dump())
    return create(session, person)


@router.get("/{person_id}", response_model=models.PersonRead)
def get_person(person_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.Person, person_id)


@router.patch("/{person_id}", response_model=models.PersonRead)
def update_person(
    person_id: int, payload: models.PersonUpdate, session: Session = Depends(get_session)
):
    person = get_or_404(session, models.Person, person_id)
    return update(session, person, payload)


@router.delete("/{person_id}", status_code=204)
def delete_person(person_id: int, session: Session = Depends(get_session)):
    person = get_or_404(session, models.Person, person_id)
    delete(session, person)
    return None
