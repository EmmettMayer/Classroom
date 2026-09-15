import argparse
import os
import sys
import time

from logtail.core import format_line, line_matches, load_config


def main():
    config = load_config()

    parser = argparse.ArgumentParser(
        description="Follow, filter, and format log files."
    )
    parser.add_argument("path", help="Path to the log file")
    parser.add_argument("-f", "--follow", action="store_true", help="Follow file appends")
    parser.add_argument("--since", help="Filter logs since timestamp")
    parser.add_argument("--level", help="Filter by log level")
    parser.add_argument("--grep", help="Filter by string/pattern")
    parser.add_argument("--json", action="store_true", help="Output JSON format")

    # Set defaults: Config file < Environment Variables < Flags
    parser.set_defaults(
        follow=os.getenv("LOGTAIL_FOLLOW", "").lower() == "true" or config.get("follow") == "true",
        since=os.getenv("LOGTAIL_SINCE") or config.get("since"),
        level=os.getenv("LOGTAIL_LEVEL") or config.get("level"),
        grep=os.getenv("LOGTAIL_GREP") or config.get("grep"),
        json=os.getenv("LOGTAIL_JSON", "").lower() == "true" or config.get("json") == "true"
    )

    args = parser.parse_args()

    # Validate file existence -> stderr + exit code 1
    if not os.path.exists(args.path):
        sys.stderr.write(f"Error: File '{args.path}' not found.\n")
        sys.exit(1)

    try:
        with open(args.path, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    if args.follow:
                        time.sleep(0.1)
                        continue
                    break

                if line_matches(line, level=args.level, grep=args.grep, since=args.since):
                    sys.stdout.write(format_line(line, args.json) + "\n")
                    sys.stdout.flush()

    except BrokenPipeError:
        # Prevents crash when piped into `head` (Requirement: no deadlock/traceback)
        sys.stdout = None
        sys.exit(0)

if __name__ == "__main__":
    main()
