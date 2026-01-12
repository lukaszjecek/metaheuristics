from __future__ import annotations

import time
from datetime import datetime, timezone

def perf_counter_s() -> float:
    return time.perf_counter()

def iso_timestamp() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

def timestamp_compact() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")