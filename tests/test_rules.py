import pytest

from app.rules import guess_category


# parametrize ejecuta la misma prueba una vez por cada par (mensaje, esperado)
@pytest.mark.parametrize(
    ("message", "expected"),
    [
        ("Could not find the UI element for selector <webctrl id='login' />", "selector"),
        ("Operation timed out after 30000 ms", "timeout"),
        ("TIMEOUT WAITING FOR APP", "timeout"),
        ("Login failed: password expired for user svc_bot", "credentials"),
        ("Invalid credentials for SAP login", "credentials"),
        ("Invoice is missing mandatory field TaxId", "business_data"),
        ("SAP returned 503 Service Unavailable", "system_down"),
        ("Something weird happened", "unknown"),
    ],
)
def test_guess_category(message: str, expected: str) -> None:
    assert guess_category(message) == expected