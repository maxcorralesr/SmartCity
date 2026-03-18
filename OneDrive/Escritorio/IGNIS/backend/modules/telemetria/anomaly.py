"""Anomaly detection: temperature spike >=20% in 5s, power cut, gas detection."""
from backend.modules.telemetry.buffer import TelemetryPoint, get_last_seconds

WINDOW_ANOMALY_SECONDS = 5
TEMPERATURE_SPIKE_RATIO = 1.20  # 20% increase
POWER_CUT_VOLTAGE_THRESHOLD = 5.0  # below this = power cut
POWER_CUT_AMPERAGE_THRESHOLD = 0.5


def check_temperature_spike(points: list[TelemetryPoint]) -> bool:
    if len(points) < 2:
        return False
    oldest = points[0].temperature
    newest = points[-1].temperature
    if oldest <= 0:
        return newest > 50  # arbitrary high if no baseline
    return newest >= oldest * TEMPERATURE_SPIKE_RATIO


def check_power_cut(points: list[TelemetryPoint]) -> bool:
    if not points:
        return False
    # Consider power cut if latest reading shows near-zero voltage/amperage
    p = points[-1]
    return p.voltage < POWER_CUT_VOLTAGE_THRESHOLD or p.amperage < POWER_CUT_AMPERAGE_THRESHOLD


def check_gas(points: list[TelemetryPoint]) -> bool:
    if not points:
        return False
    return points[-1].gas_detector is True


def detect_anomaly(branch_id: int) -> str | None:
    """
    Returns anomaly type string if detected: 'temperatura', 'corte_luz', 'gas', or None.
    Buffer already has the latest point (just pushed). Most severe: gas > temperatura > corte_luz.
    """
    points = get_last_seconds(branch_id, WINDOW_ANOMALY_SECONDS)
    if not points:
        return None

    if check_gas(points):
        return "gas"
    if check_temperature_spike(points) and check_power_cut(points):
        return "temperatura"  # transformer heat + power cut (Waldo's scenario)
    if check_temperature_spike(points):
        return "temperatura"
    if check_power_cut(points):
        return "corte_luz"
    return None
