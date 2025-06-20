import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "sqlite:///./admin.db"  # Example SQLite database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tglegram_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    registered_at = Column(DateTime, default=datetime.datetime.now)
    active = Column(Boolean, default=True)
    

class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.datetime.now)
    
    
Base.metadata.create_all(bind=engine)