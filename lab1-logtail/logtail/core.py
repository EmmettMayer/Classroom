import json
import os


def load_config():
    """Reads simple key-value defaults from ~/.logtailrc if it exists."""
    config_path = os.path.expanduser("~/.logtailrc")
    config = {}
    if os.path.exists(config_path):
        with open(config_path) as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    config[k] = v
    return config

def line_matches(line, level=None, grep=None, since=None):
    """Filters line using simple string checks."""
    if level and level.upper() not in line.upper():
        return False
    if grep and grep not in line:
        return False
    return not (since and line[:len(since)] < since)


def format_line(line, json_mode=False):
    """Formats output as clean text or JSON."""
    line_clean = line.rstrip("\n")
    if json_mode:
        return json.dumps({"message": line_clean})
    return line_clean
