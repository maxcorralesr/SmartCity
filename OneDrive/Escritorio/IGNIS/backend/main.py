"""IGNIS FastAPI application."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import CORS_ORIGINS, API_PREFIX
from backend.db.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables and seed on startup."""
    seed()
    yield
    # shutdown if needed


app = FastAPI(title="IGNIS", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from backend.modules.sucursales.router import router as sucursales_router
from backend.modules.telemetry.router import router as telemetry_router
from backend.modules.compliance.router import router as compliance_router
from backend.modules.alerts.router import router as alerts_router

app.include_router(sucursales_router, prefix=API_PREFIX)
app.include_router(telemetry_router, prefix=API_PREFIX)
app.include_router(compliance_router, prefix=API_PREFIX)
app.include_router(alerts_router)


@app.get("/health")
def health():
    return {"status": "ok"}
