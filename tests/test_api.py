from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID = {
    "robot_name": "BOT_INVOICES_01",
    "process_name": "InvoiceProcessing",
    "exception_type": "SelectorNotFound",
    "message": "Could not find the UI element for selector <webctrl id='login' />",
    "severity": "high",
    "occurred_at": "2026-10-06T10:00:00-05:00",
}


def test_health_ok():
    assert client.get("/health").status_code == 200


def test_create_exception_valid():
    r = client.post("/exceptions", json=VALID)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["severity"] == "high"


def test_create_exception_missing_message():
    payload = {k: v for k, v in VALID.items() if k != "message"}
    assert client.post("/exceptions", json=payload).status_code == 422


def test_create_exception_invalid_severity():
    payload = {**VALID, "severity": "critical"}
    assert client.post("/exceptions", json=payload).status_code == 422


def test_get_exception_not_found():
    assert client.get("/exceptions/999999999").status_code == 404
    
def test_list_exceptions_limit_too_high():
    # limit tiene máximo 100: FastAPI debe rechazar 500 antes de entrar al endpoint
    assert client.get("/exceptions", params={"limit": 500}).status_code == 422


def test_list_exceptions_filter_by_robot():
    # 1. Crear una excepción con un robot propio de esta prueba
    payload = {**VALID, "robot_name": "BOT_FILTER_TEST"}
    assert client.post("/exceptions", json=payload).status_code == 201

    # 2. Consultar filtrando por ese robot
    r = client.get("/exceptions", params={"robot_name": "BOT_FILTER_TEST"})
    assert r.status_code == 200
    results = r.json()

    # 3. Debe haber al menos un resultado y todos deben ser de ese robot
    assert len(results) > 0
    for item in results:
        assert item["robot_name"] == "BOT_FILTER_TEST"