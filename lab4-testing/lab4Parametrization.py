import pytest

def classify_http_status(status_code: int) -> str:
    """Categorizes HTTP status codes for operational logging."""
    if 200 <= status_code < 300:
        return "SUCCESS"
    elif 400 <= status_code < 500:
        return "CLIENT_ERROR"
    elif 500 <= status_code < 600:
        return "SERVER_ERROR"
    return "UNKNOWN"

@pytest.mark.parametrize("status, expected", [
    (200, "SUCCESS"),
    (404, "CLIENT_ERROR"),
    (500, "SERVER_ERROR"),
    (503, "SERVER_ERROR"),
    (999, "UNKNOWN")
])
def test_classify_http_status(status, expected):
    assert classify_http_status(status) == expected

if __name__ == "__main__":
    pytest.main([__file__])
