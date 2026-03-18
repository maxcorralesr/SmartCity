"""Seed database con Waldo's (dictamen vencido) y el Sam's Club (aprobado)."""
from datetime import date, timedelta
from backend.db.database import SessionLocal, init_db
from backend.db.models import Sucursal, AuditoriaPC


# Hermosillo centro ~29.0729, -110.9559
WALDOS_LAT, WALDOS_LNG = 29.0780, -110.9620
SAMS_LAT, SAMS_LNG = 29.0680, -110.9480


def seed():
    init_db()
    db = SessionLocal()
    try:
        if db.query(Sucursal).first() is not None:
            return  # already seeded
        # Waldo's - dictamen vencido (4 años)
        waldos = Sucursal(
            id=1,
            nombre="Waldo's",
            lat=WALDOS_LAT,
            lng=WALDOS_LNG,
            nivel_riesgo_base="medio",
        )
        db.add(waldos)
        db.add(AuditoriaPC(
            sucursal_id=1,
            fecha_ultimo_dictamen=date.today() - timedelta(days=4 * 365),
            estado="Vencido",
        ))
        # Sam's Club - aprobado
        sams = Sucursal(
            id=2,
            nombre="Sam's Club",
            lat=SAMS_LAT,
            lng=SAMS_LNG,
            nivel_riesgo_base="medio",
        )
        db.add(sams)
        db.add(AuditoriaPC(
            sucursal_id=2,
            fecha_ultimo_dictamen=date.today() - timedelta(days=30),
            estado="Aprobado",
        ))
        db.commit()
    finally:
        db.close()
