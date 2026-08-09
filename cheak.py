from database import SessionLocal
from models import Drama, DramaAspect, Aspect, UserDrama, UserPreference, Conversation

db = SessionLocal()

print("=== DRAMAS ===")
for d in db.query(Drama).all():
    print(d.id, d.title, "| synopsis:", d.synopsis, "| episodes:", d.episodes,
          "| genres:", d.genres, "| cast:", d.cast, "| network:", d.network,
          "| release_year:", d.release_year, "| country:", d.country)

print("\n=== USER_DRAMAS ===")
for u in db.query(UserDrama).all():
    print(u.id, "drama_id:", u.drama_id, "| status:", u.status,
          "| enjoyment:", u.enjoyment, "| started_at:", u.started_at,
          "| finished_at:", u.finished_at)

print("\n=== ASPECTS ===")
for a in db.query(Aspect).all():
    print(a.id, a.name, "| is_default:", a.is_default)

print("\n=== DRAMA_ASPECTS ===")
for da in db.query(DramaAspect).all():
    print(da.id, "drama_id:", da.drama_id, "| aspect_id:", da.aspect_id,
          "| score:", da.score, "| reason:", da.reason)

print("\n=== USER_PREFERENCES ===")
for p in db.query(UserPreference).all():
    print(p.id, "drama_id:", p.drama_id, "| category:", p.category,
          "| value:", p.value, "| sentiment:", p.sentiment,
          "| confidence:", p.confidence)

print("\n=== CONVERSATIONS ===")
for c in db.query(Conversation).all():
    print(c.id, "drama_id:", c.drama_id, "| role:", c.role,
          "| message:", c.message[:60], "| timestamp:", c.timestamp)

db.close()