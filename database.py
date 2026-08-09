from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AttributeType
from seed import DEFAULT_ATTRIBUTES

engine = create_engine("sqlite:///data/drama.db")

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

def seed_attribute_types(db):
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
                    name=attribute["name"]
                )
            )
        elif existing.key is None:
            existing.key = attribute["key"]

    db.commit()

Base.metadata.create_all(bind=engine)
db = SessionLocal()
seed_attribute_types(db)
db.close()