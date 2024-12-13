from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from config import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        # Prueba simple para asegurar que la conexión funcione
        db.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}