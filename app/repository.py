import psycopg

from app.schemas import ExceptionIn


def insert_exception(conn: psycopg.Connection, data: ExceptionIn) -> dict:
    # %(nombre)s = parámetro: psycopg escapa los valores, nunca se concatenan en el SQL
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


def get_exception(conn: psycopg.Connection, exception_id: int) -> dict | None:
    return conn.execute(
        """
        SELECT id, robot_name, process_name, exception_type, message, severity, occurred_at, received_at
        FROM bot_exceptions
        WHERE id = %s
        """,
        (exception_id,),
    ).fetchone()