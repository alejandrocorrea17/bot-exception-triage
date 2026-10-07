from typing import Literal

# Literal: el tipo solo admite estos valores exactos; el editor y las herramientas lo verifican
Category = Literal["selector", "timeout", "credentials", "business_data", "system_down", "unknown"]

# Lista de (categoría, palabras clave). El orden importa: gana la primera que coincida
_RULES: list[tuple[Category, tuple[str, ...]]] = [
    ("credentials", ("password", "credential", "login failed", "unauthorized", "401", "account locked")),
    ("system_down", ("503", "service unavailable", "connection refused", "host unreachable", "no route to host")),
    ("timeout", ("timeout", "timed out", "took too long")),
    ("selector", ("selector", "ui element", "element not found")),
    ("business_data", ("invalid", "mandatory", "duplicate", "not valid", "format")),
]


def guess_category(message: str) -> Category:
    """Clasifica una excepción por palabras clave. Es la línea base contra la que se medirá el LLM."""
    text = message.lower()  # comparación sin importar mayúsculas
    for category, keywords in _RULES:
        # any() se detiene en la primera palabra que aparezca dentro del texto
        if any(keyword in text for keyword in keywords):
            return category
    return "unknown"