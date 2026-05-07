from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Annotated,List
from pydantic import BaseModel

import models
from database import SessionLocal, engine

# Initialize FastAPI app
app = FastAPI()

# Allow frontend (React on localhost:3000) to call backend
# # below is a port or different application is allowed to call our api application only it is running on our local host
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
   
)



# ---------------- Pydantic Models ----------------
class TransactionBase(BaseModel):
    amount: float
    category: str
    description: str
    is_income: bool
    date: str

class TransactionModel(TransactionBase):
    id: int

    class Config:
        # from_attributes = True   # ✅ Pydantic v2 fix
        omr_mode=True

# ---------------- Dependency ----------------
# # below is the dependency injection for our application. we are trying a database connection here
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# Create tables
models.Base.metadata.create_all(bind=engine)

# ---------------- Routes ----------------
# # based on everything on the transaction base. we map all the vars in the TransactionBase to sqlite database
@app.get("/")
async def root():
    return {"message": "FastAPI Finance API is running"}

@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(transaction: TransactionBase, db: db_dependency):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions/",response_model=List[TransactionModel])
async def read_transactions(db:db_dependency,skip:int=0,limit:int=100):
    transactions=db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions
