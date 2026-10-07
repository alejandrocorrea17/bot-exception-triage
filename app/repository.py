import psycopg

from app.schemas import ExceptionIn


class ExceptionNotFoundError(Exception):
    """Se lanza cuando no existe una excepción con el id pedido."""

    def __init__(self, exception_id: int):
        super().__init__(f"Exception {exception_id} not found")
        self.exception_id = exception_id


def insert_exception(conn: psycopg.Connection, data: ExceptionIn) -> dict:
    # %(nombre)s = parámetro: psycopg envía los valores aparte, nunca se concatenan en el SQL
    row = conn.execute(
        """
        INSERT INTO bot_exceptions
            (robot_name, process_name, exception_type, message, severity, occurred_at)
        VALUES
            (%(robot_name)s, %(process_name)s, %(exception_type)s, %(message)s, %(severity)s, %(occurred_at)s)
        RETURNING id, robot_name, process_name, exception_type, message, severity, occurred_at, received_at
        """,
        data.model_dump(),
    ).fetchone()
    conn.commit()
    return row


def get_exception(conn: psycopg.Connection, exception_id: int) -> dict:
    row = conn.execute(
        """
        SELECT id, robot_name, process_name, exception_type, message, severity, occurred_at, received_at
        FROM bot_exceptions
        WHERE id = %s
        """,
        (exception_id,),
    ).fetchone()
    if row is None:
        # El repositorio no sabe de HTTP: solo dice qué pasó
        raise ExceptionNotFoundError(exception_id)
    return row