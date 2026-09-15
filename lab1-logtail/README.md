# logtail

A command-line tool to follow, filter, and format log files.

## Installation

```bash
pip install -e .

## Usage

logtail <path> [options]

Options

-f, --follow: Stream newly added log lines continuously.

--since: Filter entries starting from an ISO timestamp string.

--level: Filter entries by log level (INFO, ERROR, etc.).

--grep: Filter entries matching a string or pattern.

--json: Format output entries as JSON objects.

Options Precedence

Configuration defaults are resolved in this order:

Command Line Flags (highest priority)

Environment Variables (LOGTAIL_LEVEL, LOGTAIL_JSON, LOGTAIL_GREP, etc.)

Configuration File (~/.logtailrc) (lowest priority)

Exit Codes

0: Success (including clean exits when piped to head or other tools).

1: File not found or execution failure.

2: Command line argument parsing error.
