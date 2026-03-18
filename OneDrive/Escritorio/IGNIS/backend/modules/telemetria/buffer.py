"""In-memory circular buffer: last 60 seconds of telemetry per branch_id."""
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict

WINDOW_SECONDS = 60


@dataclass
class TelemetryPoint:
    timestamp: datetime
    temperature: float
    amperage: float
    voltage: float
    smoke_detector: bool
    gas_detector: bool


# Global buffer: branch_id -> deque of TelemetryPoint (newest at right)
_buffers: Dict[int, deque] = {}


def get_buffer(branch_id: int) -> deque:
    if branch_id not in _buffers:
        _buffers[branch_id] = deque()
    return _buffers[branch_id]


def push(branch_id: int, point: TelemetryPoint) -> None:
    buf = get_buffer(branch_id)
    buf.append(point)
    # Prune older than 60 seconds
    cutoff = point.timestamp - timedelta(seconds=WINDOW_SECONDS)
    while buf and buf[0].timestamp < cutoff:
        buf.popleft()


def get_last_seconds(branch_id: int, seconds: float) -> list[TelemetryPoint]:
    """Return points within the last `seconds` for this branch."""
    buf = get_buffer(branch_id)
    if not buf:
        return []
    newest = buf[-1].timestamp
    cutoff = newest - timedelta(seconds=seconds)
    return [p for p in buf if p.timestamp >= cutoff]


def get_all_recent(branch_id: int) -> list[TelemetryPoint]:
    """Return all points in the 60s window (for optional API)."""
    return list(get_buffer(branch_id))
