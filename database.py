"""Database configuration and default drama attribute setup."""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import AttributeType, Base
from seed import DEFAULT_ATTRIBUTES

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{(DATA_DIR / 'drama.db').as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base.metadata.create_all(bind=engine)


def seed_attribute_types() -> None:
    """Ensure the default drama attribute types exist."""
    db = SessionLocal()
    try:
        for attribute in DEFAULT_ATTRIBUTES:
            existing = db.query(AttributeType).filter_by(key=attribute["key"]).first()
            if existing is None:
                db.add(AttributeType(key=attribute["key"], name=attribute["name"]))
        db.commit()
    finally:
        db.close()


seed_attribute_types()
