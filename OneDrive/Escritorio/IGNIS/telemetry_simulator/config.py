"""Simulator configuration."""
import os

# Backend URL (override with IGNIS_BACKEND_URL env var)
BACKEND_URL = os.environ.get("IGNIS_BACKEND_URL", "http://localhost:8000")
TELEMETRY_ENDPOINT = f"{BACKEND_URL}/api/telemetry"

# Branch IDs (must match seeded DB: 1=Waldo's, 2=Sam's Club)
WALDOS_BRANCH_ID = 1
SAMS_BRANCH_ID = 2

# Interval between POSTs (seconds)
SEND_INTERVAL_SEC = 1.0

# Anomaly duration (seconds) after pressing W or S
WALDOS_ANOMALY_DURATION_SEC = 8   # two "power cuts" + temp spike over ~5s
SAMS_ANOMALY_DURATION_SEC = 6     # gas detection for a few seconds

# Normal ranges (for baseline telemetry)
NORMAL_TEMP_MIN = 22.0
NORMAL_TEMP_MAX = 28.0
NORMAL_VOLTAGE = 220.0
NORMAL_AMPERAGE = 15.0

# Waldo's anomaly: power cut (0) + temp spike (+40%)
ANOMALY_VOLTAGE_CUT = 0.0
ANOMALY_AMPERAGE_CUT = 0.0
ANOMALY_TEMP_SPIKE_FACTOR = 1.40  # 40% increase

# Sam's anomaly: gas detector on
ANOMALY_GAS_DETECTOR = True
