from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base

DATABASE_URL = "sqlite:///./data/todo.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

app = FastAPI()

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)


class ItemCreate(BaseModel):
    title: str
    description: str
    completed: bool = False

class ItemFull(BaseModel):
    id: int
    title: str
    description: str
    completed: bool = False
@app.post("/items/", response_model=ItemCreate)
def create_item(item: ItemCreate):
    db: Session = SessionLocal()
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[ItemFull])
def read_items():
    db: Session = SessionLocal()
    items = db.query(Item).all()
    return items


@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemCreate):
    db: Session = SessionLocal()
    db_item = db.query(Item).get(item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in item.model_dump().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    db: Session = SessionLocal()
    db_item = db.query(Item).get(item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted"}