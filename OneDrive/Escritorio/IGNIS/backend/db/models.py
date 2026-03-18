"""SQLAlchemy models for IGNIS."""
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Date, Boolean, Text
from sqlalchemy.orm import relationship

from backend.db.database import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    nivel_riesgo_base = Column(String(50), default="medio")  # bajo, medio, alto

    auditorias_pc = relationship("AuditoriaPC", back_populates="sucursal")
    incidentes = relationship("Incidente", back_populates="sucursal")


class AuditoriaPC(Base):
    __tablename__ = "auditorias_pc"

    id = Column(Integer, primary_key=True, index=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    fecha_ultimo_dictamen = Column(Date, nullable=False)
    estado = Column(String(50), nullable=False)  # Aprobado, Vencido

    sucursal = relationship("Sucursal", back_populates="auditorias_pc")


class Incidente(Base):
    __tablename__ = "incidentes"

    id = Column(Integer, primary_key=True, index=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String(50), nullable=False)  # temperatura, corte_luz, gas
    severidad = Column(String(50), nullable=False)  # bajo, medio, alto, critico
    detalles = Column(Text, nullable=True)
    resuelto = Column(Boolean, default=False)

    sucursal = relationship("Sucursal", back_populates="incidentes")
