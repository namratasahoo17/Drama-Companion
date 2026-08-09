from datetime import datetime, UTC


def save_metadata(db, drama, metadata):
    """Write fetched metadata onto an existing Drama row's own columns.
    (Objective fields live directly on Drama now, not in DramaAttribute.)"""

    if "episodes" in metadata:
        drama.episodes = metadata["episodes"]
    if "release_year" in metadata:
        drama.release_year = metadata["release_year"]
    if "country" in metadata:
        drama.country = metadata["country"]
    if "network" in metadata:
        drama.network = metadata["network"]
    if "synopsis" in metadata:
        drama.synopsis = metadata["synopsis"]

    if "genres" in metadata:
        genres = metadata["genres"]
        drama.genres = ",".join(genres) if isinstance(genres, list) else genres

    if "cast" in metadata:
        cast = metadata["cast"]
        drama.cast = ",".join(cast) if isinstance(cast, list) else cast

    drama.last_synced = datetime.now(UTC)
    db.commit()
    db.refresh(drama)
    return drama