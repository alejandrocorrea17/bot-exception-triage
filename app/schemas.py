from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Severity = Literal["low", "medium", "high"]


class ExceptionIn(BaseModel):
    robot_name: str = Field(min_length=1, max_length=100)
    process_name: str = Field(min_length=1, max_length=100)
    exception_type: str | None = Field(default=None, max_length=100)
    message: str = Field(min_length=1, max_length=5000)
    severity: Severity = "medium"
    occurred_at: datetime


class ExceptionOut(ExceptionIn):
    # Lo que devuelve la API: lo recibido más lo que genera la base
    id: int
    received_at: datetime