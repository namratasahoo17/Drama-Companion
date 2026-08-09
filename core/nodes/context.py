from sqlalchemy import select

from database import SessionLocal
from models import Drama
from core.state import AppState
from metadata.provider import fetch_metadata
from metadata.service import save_metadata


def drama_to_dict(drama):
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
        "aspects": aspects_to_list(drama.aspects)
    }

def aspects_to_list(aspects):
    result = []
    for a in aspects:
        result.append({
            "name": a.aspect.name,
            "score": a.score,
            "reason": a.reason,
        })
    return result

def context_node(state: AppState):
    title = state.get("drama_title")
    drama_dict = None

    if title:
        with SessionLocal() as db:
            stmt = select(Drama).where(Drama.title == title)
            drama = db.scalar(stmt)

            if drama is None:
                # unknown drama — create it and fetch metadata silently,
                # user never sees this step happen
                drama = Drama(title=title)
                db.add(drama)
                db.flush()

                metadata = fetch_metadata(title)
                if metadata is not None:
                    save_metadata(db, drama, metadata)

            drama_dict = drama_to_dict(drama)

    return {
        **state,
        "drama": drama_dict,
    }