"""Optional GET for compliance status."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.modules.compliance.service import get_compliance_status

router = APIRouter(prefix="/compliance", tags=["compliance"])


@router.get("/sucursal/{sucursal_id}")
def compliance_status(sucursal_id: int, db: Session = Depends(get_db)):
    en_regla, estado = get_compliance_status(db, sucursal_id)
    return {"sucursal_id": sucursal_id, "en_regla": en_regla, "estado": estado}
