from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ============================================================
# OBJECTIVE — Drama Knowledge (from metadata providers, never
# touched by user opinion)
# ============================================================

class Drama(Base):
    __tablename__ = "dramas"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    synopsis = Column(Text)
    episodes = Column(Integer)
    genres = Column(String)          # simple comma-separated for now, e.g. "mystery,romance"
    cast = Column(String)            # comma-separated "Actor - Character" pairs, for now
    network = Column(String)
    release_year = Column(Integer)
    country = Column(String)
    last_synced = Column(DateTime)   # when metadata was last fetched, null = never fetched

    # subjective, linked
    progress = relationship("UserDrama", backref="drama", uselist=False, cascade="all, delete-orphan")
    conversations = relationship("Conversation", backref="drama")
    aspects = relationship("DramaAspect", backref="drama", cascade="all, delete-orphan")
    attributes = relationship("DramaAttribute", backref="drama", cascade="all, delete-orphan")


# ============================================================
# SUBJECTIVE — User Knowledge (learned through conversation)
# ============================================================

class UserDrama(Base):
    """The user's relationship with one specific drama.
    Kept separate from Drama so re-fetching metadata never touches this."""
    __tablename__ = "user_dramas"

    id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, ForeignKey("dramas.id"), unique=True)
    status = Column(String)          # watching / completed / dropped / plan_to_watch
    enjoyment = Column(Float)        # overall rating, inferred or explicit
    started_at = Column(DateTime)
    finished_at = Column(DateTime)


class Aspect(Base):
    """Reusable rating dimensions, e.g. 'mystery', 'chemistry', 'pacing'."""
    __tablename__ = "aspects"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    is_default = Column(Boolean, default=False)


class DramaAspect(Base):
    """How strongly an aspect showed up in a specific drama, per the user."""
    __tablename__ = "drama_aspects"

    id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, ForeignKey("dramas.id"))
    aspect_id = Column(Integer, ForeignKey("aspects.id"))
    score = Column(Float)
    reason = Column(String)
    aspect = relationship("Aspect")


class AttributeType(Base):
    """Reusable attribute categories, e.g. 'male_lead_trait', 'trope'."""
    __tablename__ = "attribute_types"

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    name = Column(String)


class DramaAttribute(Base):
    """Specific attribute values tied to a drama, e.g. 'cute male lead'."""
    __tablename__ = "drama_attributes"

    id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, ForeignKey("dramas.id"))
    attribute_type_id = Column(Integer, ForeignKey("attribute_types.id"))
    value = Column(String)
    score = Column(Float, nullable=True)
    last_updated = Column(DateTime, nullable=True)
    attribute_type = relationship("AttributeType")


class UserPreference(Base):
    """Standing preferences about the user, NOT tied to one drama.
    E.g. 'likes psychological thrillers' — built up across many
    conversations and dramas. This is what Phase 4 (Learn) writes to."""
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True)
    category = Column(String)        # genre / trope / actor / pacing / ending_style
    value = Column(String)           # 'mystery', 'cute male lead', 'emotional ending'
    sentiment = Column(Float)        # -1.0 to 1.0
    confidence = Column(Float, default=0.5)
    source_conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    drama_id = Column(Integer, ForeignKey("dramas.id"), nullable=True)  # what triggered it, if known
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    drama_id = Column(Integer, ForeignKey("dramas.id"), nullable=True)
    role = Column(String)            # 'user' or 'assistant'
    message = Column(String)
    timestamp = Column(DateTime, server_default=func.now())


class Memory(Base):
    """Free-text long-term memories the AI has distilled and chosen to keep."""
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    memory_type = Column(String)     # 'preference_summary' / 'fact' / 'note'
    created_at = Column(DateTime, server_default=func.now())