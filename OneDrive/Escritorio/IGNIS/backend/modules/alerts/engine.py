"""Alerts engine: process incident (compliance + persist + broadcast)."""
from datetime import datetime
from sqlalchemy.orm import Session

from backend.db.models import Incidente
from backend.modules.compliance.service import get_severity
from backend.modules.alerts.router import broadcast_alert

PROTOCOLS = {
    "temperatura": "Protocolo de emergencia: Cortar suministro del transformador. Evacuación si persiste. Llamar a Protección Civil.",
    "corte_luz": "Protocolo de emergencia: Verificar instalación. Llamar a Protección Civil si hay riesgo.",
    "gas": "Protocolo de emergencia: Evacuación inmediata. No accionar equipos eléctricos. Llamar a Protección Civil y bomberos.",
}


async def process_incident(db: Session, sucursal_id: int, tipo: str, detalles: str | None = None) -> Incidente:
    """Compute severity (compliance), persist incident, broadcast to WebSocket clients."""
    severidad = get_severity(db, sucursal_id, tipo)
    protocolo = PROTOCOLS.get(tipo, "Protocolo de emergencia: Llamar a Protección Civil.")
    inc = Incidente(
        sucursal_id=sucursal_id,
        tipo=tipo,
        severidad=severidad,
        detalles=detalles,
        resuelto=False,
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    await broadcast_alert({
        "sucursal_id": sucursal_id,
        "tipo": tipo,
        "severidad": severidad,
        "protocolo": protocolo,
        "timestamp": datetime.utcnow().isoformat(),
    })
    return inc
