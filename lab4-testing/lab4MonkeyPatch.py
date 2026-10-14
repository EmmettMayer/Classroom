import subprocess
import pytest

def fetch_cli_version(binary_name: str) -> str:
    """Invokes a binary with --version and returns stdout, handling timeouts."""
    try:
        proc = subprocess.run([binary_name, "--version"], capture_output=True, text=True, timeout=2)
        if proc.returncode == 0:
            return proc.stdout.strip()
        return "UNKNOWN_VERSION"
    except subprocess.TimeoutExpired:
        return "ERROR_TIMEOUT"

def test_fetch_cli_version_timeout(monkeypatch):
    def fake_run_timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd=args[0], timeout=2)

    monkeypatch.setattr(subprocess, "run", fake_run_timeout)
    
    # Act
    result = fetch_cli_version("slow_tool")

    # Assert
    assert result == "ERROR_TIMEOUT"
    print(result)

if __name__ == "__main__":
    pytest.main(["-s", __file__])
