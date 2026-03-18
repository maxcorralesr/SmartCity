"""Telemetry ingestion: POST /api/telemetry, buffer + anomaly detection + persist on anomaly."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.schemas import TelemetryPayload
from backend.modules.telemetry.buffer import push, get_all_recent, TelemetryPoint
from backend.modules.telemetry.anomaly import detect_anomaly
from backend.modules.alerts.engine import process_incident

router = APIRouter(prefix="/telemetry", tags=["telemetry"])


@router.post("")
async def ingest_telemetry(payload: TelemetryPayload, db: Session = Depends(get_db)):
    point = TelemetryPoint(
        timestamp=payload.timestamp,
        temperature=payload.temperature,
        amperage=payload.amperage,
        voltage=payload.voltage,
        smoke_detector=payload.smoke_detector,
        gas_detector=payload.gas_detector,
    )
    push(payload.branch_id, point)
    anomaly_type = detect_anomaly(payload.branch_id)
    if anomaly_type:
        await process_incident(db, payload.branch_id, anomaly_type, detalles=None)
    return {"ok": True, "anomaly": anomaly_type}


@router.get("/buffer/{branch_id}")
def get_telemetry_buffer(branch_id: int):
    """Last 60s of telemetry for dashboard charts."""
    points = get_all_recent(branch_id)
    return [
        {
            "timestamp": p.timestamp.isoformat(),
            "temperature": p.temperature,
            "amperage": p.amperage,
            "voltage": p.voltage,
        }
        for p in points
    ]
