"""Load drama context from SQLite."""

from sqlalchemy import select

from core.state import AppState
from database import SessionLocal
from metadata.provider import fetch_metadata
from metadata.service import save_metadata
from models import Drama


def aspects_to_list(aspects):
    """Convert ORM aspect rows into dictionaries."""
    return [
        {"name": item.aspect.name, "score": item.score, "reason": item.reason}
        for item in aspects
    ]


def drama_to_dict(drama):
    """Convert a Drama model into a serializable dictionary."""
    return {
        "id": drama.id,
        "title": drama.title,
        "synopsis": drama.synopsis,
        "episodes": drama.episodes,
        "genres": drama.genres,
        "cast": drama.cast,
        "network": drama.network,
        "release_year": drama.release_year,
        "country": drama.country,
        "aspects": aspects_to_list(drama.aspects),
    }


def context_node(state: AppState):
    title = (state.get("drama_title") or "").strip()
    drama_dict = None

    if title:
        with SessionLocal() as db:
            drama = db.scalar(select(Drama).where(Drama.title.ilike(title)))

            if drama is None:
                drama = Drama(title=title)
                db.add(drama)
                db.flush()

                metadata = fetch_metadata(title)
                if metadata:
                    save_metadata(db, drama, metadata)

            db.refresh(drama)
            drama_dict = drama_to_dict(drama)

    return {**state, "drama": drama_dict}
