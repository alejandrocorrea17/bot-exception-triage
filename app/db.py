from collections.abc import Iterator

import psycopg
from psycopg.rows import dict_row

from app.config import settings


def get_connection() -> psycopg.Connection:
    # dict_row: cada fila llega como diccionario {columna: valor}
    return psycopg.connect(settings.database_url, row_factory=dict_row)


def get_db() -> Iterator[psycopg.Connection]:
    # Dependencia de FastAPI: abre la conexión, la entrega al endpoint y la cierra pase lo que pase
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()