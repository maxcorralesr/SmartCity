"""Compliance: given sucursal_id, return whether in regla and severity factor."""
from sqlalchemy.orm import Session
from backend.db.models import AuditoriaPC

SEVERITY_BASE = "medio"
SEVERITY_CRITICO = "critico"
SEVERITY_ALTO = "alto"
VENcido_MULTIPLIER = 2  # severity escalates when dictamen vencido


def get_compliance_status(db: Session, sucursal_id: int) -> tuple[bool, str]:
    """
    Returns (en_regla: bool, estado: "Aprobado" | "Vencido").
    Uses latest auditoria for that branch.
    """
    aud = (
        db.query(AuditoriaPC)
        .filter(AuditoriaPC.sucursal_id == sucursal_id)
        .order_by(AuditoriaPC.fecha_ultimo_dictamen.desc())
        .first()
    )
    if not aud:
        return True, "Aprobado"  # no record = assume ok
    return (aud.estado == "Aprobado", aud.estado)


def get_severity(db: Session, sucursal_id: int, base_tipo: str) -> str:
    """
    Base severity from incident type; multiply to critico if dictamen vencido.
    """
    en_regla, estado = get_compliance_status(db, sucursal_id)
    base_severity = SEVERITY_ALTO if base_tipo in ("gas", "temperatura") else SEVERITY_BASE
    if not en_regla and estado == "Vencido":
        return SEVERITY_CRITICO
    return base_severity
