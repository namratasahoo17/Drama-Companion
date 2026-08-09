from database import SessionLocal
from models import Drama, UserDrama, Aspect, DramaAspect, UserPreference, Conversation


def save_review(data, drama_id=None):
    """Save extracted review data. If drama_id is given (from an existing
    Context lookup), reuse that drama instead of creating a duplicate.
    Aspects are upserted (updated if they already exist for this drama)
    instead of duplicated on every save."""
    db = SessionLocal()
    try:
        if drama_id:
            drama = db.query(Drama).filter_by(id=drama_id).first()
        else:
            drama = db.query(Drama).filter_by(title=data["title"]).first()

        if drama is None:
            drama = Drama(title=data["title"])
            db.add(drama)
            db.flush()

        # status/enjoyment live on UserDrama, not Drama
        user_drama = db.query(UserDrama).filter_by(drama_id=drama.id).first()
        if user_drama is None:
            user_drama = UserDrama(drama_id=drama.id)
            db.add(user_drama)

        user_drama.status = "completed"
        user_drama.enjoyment = data["overall_rating"]

        for aspect_data in data["aspects"]:
            name = aspect_data["name"].strip().lower()  # normalize casing

            aspect = db.query(Aspect).filter_by(name=name).first()
            if aspect is None:
                aspect = Aspect(name=name, is_default=False)
                db.add(aspect)
                db.flush()

            drama_aspect = db.query(DramaAspect).filter_by(
                drama_id=drama.id, aspect_id=aspect.id
            ).first()

            if drama_aspect is None:
                drama_aspect = DramaAspect(drama_id=drama.id, aspect_id=aspect.id)
                db.add(drama_aspect)

            drama_aspect.score = aspect_data["score"]
            drama_aspect.reason = aspect_data["reason"]

        db.commit()
        db.refresh(drama)
        return drama
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def save_preferences(data, drama_id=None):
    db = SessionLocal()
    try:
        for pref in data:
            db.add(UserPreference(
                category=pref["category"],
                value=pref["value"],
                sentiment=pref["sentiment"],
                drama_id=drama_id,
            ))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def save_conversation(role, message, drama_id=None):
    db = SessionLocal()
    try:
        db.add(Conversation(drama_id=drama_id, role=role, message=message))
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()