"""Operaciones CRUD reutilizables."""
from typing import Iterable, TypeVar

from sqlmodel import Session, SQLModel, select

ModelType = TypeVar("ModelType", bound=SQLModel)


def get_or_404(session: Session, model: type[ModelType], object_id: int) -> ModelType:
    """Obtiene un registro o lanza una excepción 404."""

    instance = session.get(model, object_id)
    if not instance:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail=f"{model.__name__} no encontrado")
    return instance


def list_all(session: Session, model: type[ModelType]) -> Iterable[ModelType]:
    """Devuelve todos los registros del modelo."""

    return session.exec(select(model)).all()


def create(session: Session, instance: ModelType) -> ModelType:
    """Inserta un nuevo registro."""

    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def update(session: Session, instance: ModelType, data: SQLModel) -> ModelType:
    """Actualiza un registro con los campos proporcionados."""

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(instance, key, value)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def delete(session: Session, instance: ModelType) -> None:
    """Elimina un registro."""

    session.delete(instance)
    session.commit()
