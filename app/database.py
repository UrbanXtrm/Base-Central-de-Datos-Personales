"""Gestión de la base de datos."""
from contextlib import contextmanager
from typing import Iterator

from sqlmodel import Session, SQLModel, create_engine

from .config import get_settings


def get_engine():
    """Crea el motor de base de datos a partir de la configuración."""

    settings = get_settings()
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, echo=False, connect_args=connect_args)


engine = get_engine()


@contextmanager
def session_scope() -> Iterator[Session]:
    """Proporciona un contexto de sesión SQLModel."""

    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """Crea las tablas si no existen."""

    SQLModel.metadata.create_all(engine)
