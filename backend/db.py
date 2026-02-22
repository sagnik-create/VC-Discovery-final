from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    website = Column(String)
    industry = Column(String)
    stage = Column(String)
    location = Column(String)

class EnrichedCompany(Base):
    __tablename__ = "enriched_companies"

    url = Column(String, primary_key=True, index=True)
    summary = Column(String)
    whatTheyDo = Column(JSON)
    keywords = Column(JSON)
    signals = Column(JSON)
    sources = Column(JSON)
    enrichedAt = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)