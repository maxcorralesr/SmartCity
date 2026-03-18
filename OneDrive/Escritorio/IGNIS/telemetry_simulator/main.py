"""
IGNIS Telemetry Simulator.
Sends JSON payload every second to the backend. Press W for Waldo's anomaly, S for Sam's Club gas.
"""
import json
import random
import sys
import time
from datetime import datetime, timezone
from threading import Thread

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# Optional: keyboard listener (works on Windows/Linux; may need admin on Linux for global hotkeys)
try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

try:
    import threading
    KEYBOARD_THREAD = True
except ImportError:
    KEYBOARD_THREAD = False

from telemetry_simulator.config import (
    TELEMETRY_ENDPOINT,
    WALDOS_BRANCH_ID,
    SAMS_BRANCH_ID,
    SEND_INTERVAL_SEC,
    WALDOS_ANOMALY_DURATION_SEC,
    SAMS_ANOMALY_DURATION_SEC,
    NORMAL_TEMP_MIN,
    NORMAL_TEMP_MAX,
    NORMAL_VOLTAGE,
    NORMAL_AMPERAGE,
    ANOMALY_VOLTAGE_CUT,
    ANOMALY_AMPERAGE_CUT,
    ANOMALY_TEMP_SPIKE_FACTOR,
    ANOMALY_GAS_DETECTOR,
)

# Global state: which anomaly is active and until when (epoch time)
waldos_anomaly_until = 0.0
sams_anomaly_until = 0.0
# Baseline temp for Waldo's (so we can spike from it)
waldos_baseline_temp = (NORMAL_TEMP_MIN + NORMAL_TEMP_MAX) / 2


def make_payload(branch_id: int, temperature: float, voltage: float, amperage: float,
                 smoke_detector: bool, gas_detector: bool) -> dict:
    return {
        "branch_id": branch_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(temperature, 2),
        "amperage": round(amperage, 2),
        "voltage": round(voltage, 2),
        "smoke_detector": smoke_detector,
        "gas_detector": gas_detector,
    }


def send_telemetry(payload: dict) -> bool:
    try:
        r = requests.post(TELEMETRY_ENDPOINT, json=payload, timeout=2)
        if r.status_code == 200:
            data = r.json()
            anomaly = data.get("anomaly")
            if anomaly:
                print(f" [BACKEND DETECTED ANOMALY: {anomaly}]")
            return True
        print(f" [HTTP {r.status_code}]")
        return False
    except Exception as e:
        print(f" [Error: {e}]")
        return False


def get_waldos_values(now: float) -> tuple[float, float, float]:
    global waldos_baseline_temp
    if now < waldos_anomaly_until:
        # First ~2s: power cut (0), then temp starts rising; next ~3s full spike
        elapsed = (waldos_anomaly_until - now)  # seconds left in anomaly
        if elapsed > WALDOS_ANOMALY_DURATION_SEC - 2:
            voltage = ANOMALY_VOLTAGE_CUT
            amperage = ANOMALY_AMPERAGE_CUT
            temp = waldos_baseline_temp
        else:
            voltage = ANOMALY_VOLTAGE_CUT
            amperage = ANOMALY_AMPERAGE_CUT
            # Ramp temp up to 40% over baseline
            progress = 1 - (elapsed / (WALDOS_ANOMALY_DURATION_SEC - 2))
            temp = waldos_baseline_temp * (1 + (ANOMALY_TEMP_SPIKE_FACTOR - 1) * min(1.0, progress))
        return temp, voltage, amperage
    waldos_baseline_temp = NORMAL_TEMP_MIN + (NORMAL_TEMP_MAX - NORMAL_TEMP_MIN) * random.random()
    return waldos_baseline_temp, NORMAL_VOLTAGE, NORMAL_AMPERAGE


def get_sams_values(now: float) -> tuple[float, float, float, bool]:
    if now < sams_anomaly_until:
        temp = NORMAL_TEMP_MIN + (NORMAL_TEMP_MAX - NORMAL_TEMP_MIN) * random.random()
        return temp, NORMAL_VOLTAGE, NORMAL_AMPERAGE, ANOMALY_GAS_DETECTOR
    return (
        NORMAL_TEMP_MIN + (NORMAL_TEMP_MAX - NORMAL_TEMP_MIN) * random.random(),
        NORMAL_VOLTAGE,
        NORMAL_AMPERAGE,
        False,
    )


def keyboard_listener():
    """Listen for W and S keys (Windows: msvcrt; fallback: input thread)."""
    global waldos_anomaly_until, sams_anomaly_until
    print("Keyboard: Press W (Waldo's) or S (Sam's Club) for anomaly. Ctrl+C to exit.")
    if HAS_MSVCRT:
        while True:
            if msvcrt.kbhit():
                ch = msvcrt.getch().decode("utf-8", errors="ignore").lower()
                now = time.time()
                if ch == "w":
                    waldos_anomaly_until = now + WALDOS_ANOMALY_DURATION_SEC
                    print("\n>>> WALDOS ANOMALY TRIGGERED (corte luz + pico temperatura)")
                elif ch == "s":
                    sams_anomaly_until = now + SAMS_ANOMALY_DURATION_SEC
                    print("\n>>> SAMS CLUB ANOMALY TRIGGERED (gas detector)")
            time.sleep(0.1)
    else:
        # Unix: simple input loop in thread
        while True:
            try:
                line = input().strip().lower()
                now = time.time()
                if line == "w":
                    waldos_anomaly_until = now + WALDOS_ANOMALY_DURATION_SEC
                    print(">>> WALDOS ANOMALY TRIGGERED")
                elif line == "s":
                    sams_anomaly_until = now + SAMS_ANOMALY_DURATION_SEC
                    print(">>> SAMS CLUB ANOMALY TRIGGERED")
            except EOFError:
                break


def main():
    global waldos_anomaly_until, sams_anomaly_until
    print(f"IGNIS Telemetry Simulator -> {TELEMETRY_ENDPOINT}")
    print("Sending every", SEND_INTERVAL_SEC, "second(s). Branch 1=Waldo's, 2=Sam's Club.")
    # Start keyboard thread (Windows: msvcrt in main thread would block; run send loop in main and keys in thread)
    if HAS_MSVCRT:
        t = Thread(target=keyboard_listener, daemon=True)
        t.start()
    else:
        t = Thread(target=keyboard_listener, daemon=True)
        t.start()

    while True:
        now = time.time()
        # Branch 1 - Waldo's
        t1, v1, a1 = get_waldos_values(now)
        p1 = make_payload(WALDOS_BRANCH_ID, t1, v1, a1, False, False)
        print(f"POST branch_id=1 (Waldo's) temp={p1['temperature']} V={p1['voltage']} A={p1['amperage']}", end="")
        send_telemetry(p1)

        now = time.time()
        # Branch 2 - Sam's Club
        t2, v2, a2, gas2 = get_sams_values(now)
        p2 = make_payload(SAMS_BRANCH_ID, t2, v2, a2, False, gas2)
        print(f"POST branch_id=2 (Sam's) temp={p2['temperature']} gas={p2['gas_detector']}", end="")
        send_telemetry(p2)

        time.sleep(SEND_INTERVAL_SEC)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye.")
