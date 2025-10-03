"""Rutas para registros asociados a personas."""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from .. import models
from ..crud import create, delete, get_or_404, list_all, update
from ..database import engine

router = APIRouter(prefix="/records", tags=["records"])


def get_session() -> Session:
    with Session(engine) as session:
        yield session


@router.get("/medical", response_model=list[models.MedicalRecordRead])
def list_medical_records(session: Session = Depends(get_session)):
    return list_all(session, models.MedicalRecord)


@router.post("/medical", response_model=models.MedicalRecordRead, status_code=201)
def create_medical_record(
    payload: models.MedicalRecordCreate, session: Session = Depends(get_session)
):
    record = models.MedicalRecord.model_validate(payload.model_dump())
    return create(session, record)


@router.get("/medical/{record_id}", response_model=models.MedicalRecordRead)
def get_medical_record(record_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.MedicalRecord, record_id)


@router.patch("/medical/{record_id}", response_model=models.MedicalRecordRead)
def update_medical_record(
    record_id: int, payload: models.MedicalRecordUpdate, session: Session = Depends(get_session)
):
    record = get_or_404(session, models.MedicalRecord, record_id)
    return update(session, record, payload)


@router.delete("/medical/{record_id}", status_code=204)
def delete_medical_record(record_id: int, session: Session = Depends(get_session)):
    record = get_or_404(session, models.MedicalRecord, record_id)
    delete(session, record)
    return None


@router.get("/education", response_model=list[models.EducationRecordRead])
def list_education_records(session: Session = Depends(get_session)):
    return list_all(session, models.EducationRecord)


@router.post("/education", response_model=models.EducationRecordRead, status_code=201)
def create_education_record(
    payload: models.EducationRecordCreate, session: Session = Depends(get_session)
):
    record = models.EducationRecord.model_validate(payload.model_dump())
    return create(session, record)


@router.get("/education/{record_id}", response_model=models.EducationRecordRead)
def get_education_record(record_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.EducationRecord, record_id)


@router.patch("/education/{record_id}", response_model=models.EducationRecordRead)
def update_education_record(
    record_id: int, payload: models.EducationRecordUpdate, session: Session = Depends(get_session)
):
    record = get_or_404(session, models.EducationRecord, record_id)
    return update(session, record, payload)


@router.delete("/education/{record_id}", status_code=204)
def delete_education_record(record_id: int, session: Session = Depends(get_session)):
    record = get_or_404(session, models.EducationRecord, record_id)
    delete(session, record)
    return None


@router.get("/employment", response_model=list[models.EmploymentRecordRead])
def list_employment_records(session: Session = Depends(get_session)):
    return list_all(session, models.EmploymentRecord)


@router.post("/employment", response_model=models.EmploymentRecordRead, status_code=201)
def create_employment_record(
    payload: models.EmploymentRecordCreate, session: Session = Depends(get_session)
):
    record = models.EmploymentRecord.model_validate(payload.model_dump())
    return create(session, record)


@router.get("/employment/{record_id}", response_model=models.EmploymentRecordRead)
def get_employment_record(record_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.EmploymentRecord, record_id)


@router.patch("/employment/{record_id}", response_model=models.EmploymentRecordRead)
def update_employment_record(
    record_id: int, payload: models.EmploymentRecordUpdate, session: Session = Depends(get_session)
):
    record = get_or_404(session, models.EmploymentRecord, record_id)
    return update(session, record, payload)


@router.delete("/employment/{record_id}", status_code=204)
def delete_employment_record(record_id: int, session: Session = Depends(get_session)):
    record = get_or_404(session, models.EmploymentRecord, record_id)
    delete(session, record)
    return None


@router.get("/social", response_model=list[models.SocialSecurityRecordRead])
def list_social_security_records(session: Session = Depends(get_session)):
    return list_all(session, models.SocialSecurityRecord)


@router.post("/social", response_model=models.SocialSecurityRecordRead, status_code=201)
def create_social_security_record(
    payload: models.SocialSecurityRecordCreate, session: Session = Depends(get_session)
):
    record = models.SocialSecurityRecord.model_validate(payload.model_dump())
    return create(session, record)


@router.get("/social/{record_id}", response_model=models.SocialSecurityRecordRead)
def get_social_security_record(record_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.SocialSecurityRecord, record_id)


@router.patch("/social/{record_id}", response_model=models.SocialSecurityRecordRead)
def update_social_security_record(
    record_id: int, payload: models.SocialSecurityRecordUpdate, session: Session = Depends(get_session)
):
    record = get_or_404(session, models.SocialSecurityRecord, record_id)
    return update(session, record, payload)


@router.delete("/social/{record_id}", status_code=204)
def delete_social_security_record(record_id: int, session: Session = Depends(get_session)):
    record = get_or_404(session, models.SocialSecurityRecord, record_id)
    delete(session, record)
    return None


@router.get("/documents", response_model=list[models.DocumentRead])
def list_documents(session: Session = Depends(get_session)):
    return list_all(session, models.Document)


@router.post("/documents", response_model=models.DocumentRead, status_code=201)
def create_document(payload: models.DocumentCreate, session: Session = Depends(get_session)):
    document = models.Document.model_validate(payload.model_dump())
    return create(session, document)


@router.get("/documents/{document_id}", response_model=models.DocumentRead)
def get_document(document_id: int, session: Session = Depends(get_session)):
    return get_or_404(session, models.Document, document_id)


@router.patch("/documents/{document_id}", response_model=models.DocumentRead)
def update_document(
    document_id: int, payload: models.DocumentUpdate, session: Session = Depends(get_session)
):
    document = get_or_404(session, models.Document, document_id)
    return update(session, document, payload)


@router.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, session: Session = Depends(get_session)):
    document = get_or_404(session, models.Document, document_id)
    delete(session, document)
    return None
