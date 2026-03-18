"""Pydantic schemas for IGNIS API."""
from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel


# --- Telemetry (Ingesta) ---
class TelemetryPayload(BaseModel):
    branch_id: int
    timestamp: datetime
    temperature: float
    amperage: float
    voltage: float
    smoke_detector: bool
    gas_detector: bool


# --- Sucursales ---
class SucursalBase(BaseModel):
    nombre: str
    lat: float
    lng: float
    nivel_riesgo_base: str = "medio"


class SucursalCreate(SucursalBase):
    pass


class AuditoriaPCResponse(BaseModel):
    id: int
    sucursal_id: int
    fecha_ultimo_dictamen: date
    estado: str

    class Config:
        from_attributes = True


class SucursalResponse(SucursalBase):
    id: int

    class Config:
        from_attributes = True


class SucursalDetailResponse(SucursalResponse):
    auditorias_pc: List[AuditoriaPCResponse] = []

    class Config:
        from_attributes = True


# --- Incidentes ---
class IncidenteResponse(BaseModel):
    id: int
    sucursal_id: int
    timestamp: datetime
    tipo: str
    severidad: str
    detalles: Optional[str] = None
    resuelto: bool = False

    class Config:
        from_attributes = True


# --- WebSocket alert message ---
class AlertMessage(BaseModel):
    sucursal_id: int
    tipo: str
    severidad: str
    protocolo: str
    timestamp: Optional[datetime] = None
