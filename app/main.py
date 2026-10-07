import psycopg
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse

from app import repository
from app.db import get_connection, get_db
from app.schemas import ExceptionIn, ExceptionOut

app = FastAPI(title="Bot Exception Triage")


@app.get("/health")
def health():
    # Conexión propia, no la dependencia: si la base cae queremos 503 controlado, no un 500
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return {"status": "ok"}
    except psycopg.OperationalError:
        return JSONResponse(status_code=503, content={"status": "db_unavailable"})


@app.post("/exceptions", response_model=ExceptionOut, status_code=status.HTTP_201_CREATED)
def create_exception(payload: ExceptionIn, conn: psycopg.Connection = Depends(get_db)):
    return repository.insert_exception(conn, payload)


@app.get("/exceptions/{exception_id}", response_model=ExceptionOut)
def read_exception(exception_id: int, conn: psycopg.Connection = Depends(get_db)):
    try:
        return repository.get_exception(conn, exception_id)
    except repository.ExceptionNotFoundError as exc:
        # La API traduce el error de dominio a un código HTTP
        raise HTTPException(status_code=404, detail=str(exc)) from exc