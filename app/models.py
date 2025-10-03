"""Modelos de datos principales."""
from datetime import date
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class PersonBase(SQLModel):
    """Campos compartidos para una persona."""

    first_name: str = Field(description="Nombre")
    last_name: str = Field(description="Apellidos")
    email: Optional[str] = Field(default=None, description="Correo electrónico")
    phone: Optional[str] = Field(default=None, description="Teléfono de contacto")
    date_of_birth: Optional[date] = Field(default=None, description="Fecha de nacimiento")
    nationality: Optional[str] = Field(default=None, description="Nacionalidad")
    address: Optional[str] = Field(default=None, description="Dirección principal")


class Person(PersonBase, table=True):
    """Tabla que representa a una persona."""

    id: Optional[int] = Field(default=None, primary_key=True)

    medical_records: list["MedicalRecord"] = Relationship(back_populates="person")
    education_records: list["EducationRecord"] = Relationship(back_populates="person")
    employment_records: list["EmploymentRecord"] = Relationship(back_populates="person")
    social_security_records: list["SocialSecurityRecord"] = Relationship(back_populates="person")
    documents: list["Document"] = Relationship(back_populates="person")


class PersonCreate(PersonBase):
    """Payload para crear una persona."""


class PersonRead(PersonBase):
    """Representación de lectura de una persona."""

    id: int


class PersonUpdate(SQLModel):
    """Campos editables en una persona."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[date] = None
    nationality: Optional[str] = None
    address: Optional[str] = None


class MedicalRecordBase(SQLModel):
    """Información médica general."""

    title: str = Field(description="Diagnóstico o episodio")
    description: Optional[str] = Field(default=None, description="Descripción detallada")
    allergies: Optional[str] = Field(default=None, description="Alergias relevantes")
    medications: Optional[str] = Field(default=None, description="Tratamientos activos")
    recorded_at: date = Field(default_factory=date.today, description="Fecha del registro")


class MedicalRecord(MedicalRecordBase, table=True):
    """Historial médico asociado a una persona."""

    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates="medical_records")


class MedicalRecordCreate(MedicalRecordBase):
    """Payload de creación."""

    person_id: int


class MedicalRecordRead(MedicalRecordBase):
    """Representación de lectura."""

    id: int
    person_id: int


class MedicalRecordUpdate(SQLModel):
    """Campos editables de un registro médico."""

    title: Optional[str] = None
    description: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    recorded_at: Optional[date] = None


class EducationRecordBase(SQLModel):
    """Información educativa."""

    institution: str = Field(description="Institución educativa")
    degree: str = Field(description="Título o certificación")
    field_of_study: Optional[str] = Field(default=None, description="Área de estudio")
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    description: Optional[str] = Field(default=None)


class EducationRecord(EducationRecordBase, table=True):
    """Registro educativo."""

    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates="education_records")


class EducationRecordCreate(EducationRecordBase):
    person_id: int


class EducationRecordRead(EducationRecordBase):
    id: int
    person_id: int


class EducationRecordUpdate(SQLModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


class EmploymentRecordBase(SQLModel):
    """Historial laboral."""

    company: str = Field(description="Empresa")
    position: str = Field(description="Puesto")
    responsibilities: Optional[str] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    achievements: Optional[str] = Field(default=None)


class EmploymentRecord(EmploymentRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates="employment_records")


class EmploymentRecordCreate(EmploymentRecordBase):
    person_id: int


class EmploymentRecordRead(EmploymentRecordBase):
    id: int
    person_id: int


class EmploymentRecordUpdate(SQLModel):
    company: Optional[str] = None
    position: Optional[str] = None
    responsibilities: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    achievements: Optional[str] = None


class SocialSecurityRecordBase(SQLModel):
    """Información de seguridad social."""

    provider: str = Field(description="Entidad administradora")
    affiliation_number: str = Field(description="Número de afiliación")
    coverage_details: Optional[str] = Field(default=None)
    effective_from: Optional[date] = Field(default=None)
    effective_to: Optional[date] = Field(default=None)


class SocialSecurityRecord(SocialSecurityRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates="social_security_records")


class SocialSecurityRecordCreate(SocialSecurityRecordBase):
    person_id: int


class SocialSecurityRecordRead(SocialSecurityRecordBase):
    id: int
    person_id: int


class SocialSecurityRecordUpdate(SQLModel):
    provider: Optional[str] = None
    affiliation_number: Optional[str] = None
    coverage_details: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None


class DocumentBase(SQLModel):
    """Metadatos de documentos asociados."""

    name: str = Field(description="Nombre del documento")
    category: str = Field(description="Categoría del documento")
    url: Optional[str] = Field(default=None, description="Ubicación en almacenamiento en la nube")
    description: Optional[str] = Field(default=None)


class Document(DocumentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    person: Person = Relationship(back_populates="documents")


class DocumentCreate(DocumentBase):
    person_id: int


class DocumentRead(DocumentBase):
    id: int
    person_id: int


class DocumentUpdate(SQLModel):
    name: Optional[str] = None
    category: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
