from datetime import datetime


def log(msg: str) -> None:
    """Simple print-based logger for local debugging.

    Prefixes messages with UTC timestamp so prints are easier to read in logs.
    """
    ts = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
    print(f"[backend] {ts} - {msg}")
