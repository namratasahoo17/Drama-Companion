"""Database configuration and default drama attribute setup."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AttributeType
from seed import DEFAULT_ATTRIBUTES

# SQLite path is stored under the project data folder.
engine = create_engine("sqlite:///data/drama.db")
SessionLocal = sessionmaker(bind=engine)

# Create tables on startup if they do not already exist.
Base.metadata.create_all(bind=engine)


def seed_attribute_types() -> None:
    """Ensure default drama attribute types exist in the database."""
    db = SessionLocal()
    try:
        for attribute in DEFAULT_ATTRIBUTES:
            existing = (
                db.query(AttributeType)
                .filter_by(name=attribute["name"])
                .first()
            )

            if existing is None:
                db.add(
                    AttributeType(
                        key=attribute["key"],
                        name=attribute["name"],
                    )
                )
            elif existing.key is None:
                existing.key = attribute["key"]

        db.commit()
    finally:
        db.close()


seed_attribute_types()
