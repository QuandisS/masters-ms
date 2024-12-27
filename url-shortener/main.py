from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import string
import random

DATABASE_URL = "sqlite:///./data/url-shortener.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

app = FastAPI()

class URLMapping(Base):
    __tablename__ = "url_mappings"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, index=True)
    short_id = Column(String, unique=True, index=True)
    clicks = Column(Integer, default=-1)

Base.metadata.create_all(bind=engine)

class URLCreate(BaseModel):
    original_url: str

def generate_short_id(lenght=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(lenght))

@app.post("/shorten/")
def shorten_url(url: URLCreate):
    db: Session = SessionLocal()
    short_id = generate_short_id()

    while db.query(URLMapping).filter_by(short_id=short_id).first():
        short_id = generate_short_id()

    db_url = URLMapping(original_url=url.original_url, short_id=short_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return {"url": f"http://localhost:8000/{db_url.short_id}"}

@app.get("/{short_id}")
def redirect_url(short_id: str):
    db: Session = SessionLocal()
    db_url = db.query(URLMapping).filter_by(short_id=short_id).first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short ID not found")

    if db_url.clicks == -1:
        db_url.clicks = 0
    db_url.clicks += 1
    db.commit()

    return RedirectResponse(url=db_url.original_url)

@app.get("/stats/{short_id}")
def get_stats(short_id: str):
    db: Session = SessionLocal()
    db_url = db.query(URLMapping).filter_by(short_id=short_id).first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "clicks": db_url.clicks,
        "original_url": db_url.original_url,
        "short_id": db_url.short_id
    }