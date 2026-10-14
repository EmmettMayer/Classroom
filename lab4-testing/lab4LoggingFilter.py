import logging
import sys

class RedactingFilter(logging.Filter):
    def __init__(self, patterns: set[str]):
        super().__init__()
        self.patterns = patterns

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        for pattern in self.patterns:
            message = message.replace(pattern, "***Redacted***")

        record.msg = message
        record.args = ()
        return True


# Test implementation
log = logging.getLogger("secure_app")
handler = logging.StreamHandler(sys.stderr)

# Attach filter
sensitive_words = {"super_secret_password", "token_9988"}
redact_filter = RedactingFilter(patterns=sensitive_words)
handler.addFilter(redact_filter)

log.addHandler(handler)
log.setLevel(logging.INFO)

log.info("User authenticated with token_9988 successfully.")
log.info("Attempted login with password super_secret_password failed.")
