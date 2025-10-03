"""Rutas para obtener la ficha completa de una persona."""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from .. import models
from ..crud import get_or_404
from ..database import engine

router = APIRouter(prefix="/profiles", tags=["profiles"])


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@router.get("/{person_id}")
def get_profile(person_id: int, session: Session = Depends(get_session)):
    """Devuelve un perfil enriquecido con todos los registros relacionados."""

    person = get_or_404(session, models.Person, person_id)
    medical = session.exec(
        select(models.MedicalRecord).where(models.MedicalRecord.person_id == person_id)
    ).all()
    education = session.exec(
        select(models.EducationRecord).where(models.EducationRecord.person_id == person_id)
    ).all()
    employment = session.exec(
        select(models.EmploymentRecord).where(models.EmploymentRecord.person_id == person_id)
    ).all()
    social = session.exec(
        select(models.SocialSecurityRecord).where(models.SocialSecurityRecord.person_id == person_id)
    ).all()
    documents = session.exec(
        select(models.Document).where(models.Document.person_id == person_id)
    ).all()
    return {
        "person": models.PersonRead.model_validate(person).model_dump(),
        "medical_records": [
            models.MedicalRecordRead.model_validate(item).model_dump() for item in medical
        ],
        "education_records": [
            models.EducationRecordRead.model_validate(item).model_dump() for item in education
        ],
        "employment_records": [
            models.EmploymentRecordRead.model_validate(item).model_dump() for item in employment
        ],
        "social_security_records": [
            models.SocialSecurityRecordRead.model_validate(item).model_dump() for item in social
        ],
        "documents": [models.DocumentRead.model_validate(item).model_dump() for item in documents],
    }
