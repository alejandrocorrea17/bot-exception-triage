import sys
import time

import httpx

from app.config import settings


def ask_ollama(prompt: str, timeout_seconds: float = 60.0) -> str:
    # stream False: Ollama devuelve la respuesta completa en un solo JSON
    response = httpx.post(
        f"{settings.ollama_url}/api/generate",
        json={"model": settings.ollama_model, "prompt": prompt, "stream": False},
        timeout=timeout_seconds,
    )
    # Convierte respuestas 4xx y 5xx en excepción en vez de seguir con datos inválidos
    response.raise_for_status()
    return response.json()["response"]


def main() -> int:
    prompt = "Classify this RPA error in one word: Selector not found on login page"
    start = time.perf_counter()  # reloj de alta precisión para medir duraciones
    try:
        answer = ask_ollama(prompt)
    except httpx.ConnectError:
        print(f"No se pudo conectar a Ollama en {settings.ollama_url}. ¿Está corriendo?")
        return 1
    except httpx.TimeoutException:
        print("Ollama no respondió a tiempo.")
        return 1
    except httpx.HTTPStatusError as exc:
        print(f"Ollama respondió {exc.response.status_code}: {exc.response.text}")
        return 1
    elapsed = time.perf_counter() - start
    print(f"Modelo: {settings.ollama_model}")
    print(f"Respuesta: {answer.strip()}")
    print(f"Tiempo: {elapsed:.2f} s")
    return 0


if __name__ == "__main__":
    # El código de salida le dice a quien ejecutó el script si terminó bien (0) o mal (1)
    sys.exit(main())