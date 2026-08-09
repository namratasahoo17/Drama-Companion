from database import SessionLocal
from models import Drama
from metadata.provider import fetch_metadata
from metadata.service import save_metadata

db = SessionLocal()

# Get an existing drama
drama = db.query(Drama).first()

metadata = fetch_metadata(drama.title)

save_metadata(db, drama, metadata)

db.commit()

db.close()

print("Metadata saved!")