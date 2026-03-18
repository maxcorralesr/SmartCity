"""Sucursales API - list and detail."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.database import get_db
from backend.db.models import Sucursal
from backend.db.schemas import SucursalResponse, SucursalDetailResponse

router = APIRouter(prefix="/sucursales", tags=["sucursales"])


@router.get("", response_model=list[SucursalResponse])
def list_sucursales(db: Session = Depends(get_db)):
    return db.query(Sucursal).all()


@router.get("/{sucursal_id}", response_model=SucursalDetailResponse)
def get_sucursal(sucursal_id: int, db: Session = Depends(get_db)):
    s = db.query(Sucursal).filter(Sucursal.id == sucursal_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return s
