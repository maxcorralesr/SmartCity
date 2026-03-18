# IGNIS - Smart City Hermosillo

Monitoreo en vivo de sucursales con telemetría, cumplimiento PC y alertas en tiempo real.

## Requisitos

- Python 3.10+
- Navegador moderno

## Cómo parar todo

En cada terminal donde algo está corriendo:

1. Pulsa **Ctrl+C** para detener el proceso (backend, simulador o servidor del frontend).
2. Repite en las otras terminales hasta que no quede nada en marcha.

No hace falta cerrar el navegador; solo las terminales donde ejecutaste los comandos.

---

## Cómo arrancar de nuevo

Abre **3 terminales** (en Cursor: Terminal → New Terminal, o PowerShell/CMD).

### Terminal 1 – Backend

```powershell
cd c:\Users\maxco\OneDrive\Escritorio\IGNIS
$env:PYTHONPATH = "c:\Users\maxco\OneDrive\Escritorio\IGNIS"
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Deja esta terminal abierta. Cuando veas algo como "Uvicorn running on http://0.0.0.0:8000", el backend está listo.

### Terminal 2 – Frontend (servidor web)

```powershell
cd c:\Users\maxco\OneDrive\Escritorio\IGNIS\frontend
python -m http.server 5500
```

Deja esta terminal abierta. Abre el navegador en **http://localhost:5500**.

### Terminal 3 – Simulador (para enviar telemetría y usar W/S)

```powershell
cd c:\Users\maxco\OneDrive\Escritorio\IGNIS
$env:PYTHONPATH = "c:\Users\maxco\OneDrive\Escritorio\IGNIS"
python -m telemetry_simulator.main
```

Aquí puedes pulsar **W** o **S** para simular anomalías. Esta terminal debe tener el foco para que las teclas funcionen.

---

## Resumen rápido

| Qué parar / arrancar | Cómo parar | Cómo arrancar |
|----------------------|------------|----------------|
| Backend              | Ctrl+C en su terminal | `python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000` (con PYTHONPATH y desde IGNIS) |
| Frontend             | Ctrl+C en su terminal | `python -m http.server 5500` (desde `frontend/`) |
| Simulador            | Ctrl+C en su terminal | `python -m telemetry_simulator.main` (con PYTHONPATH y desde IGNIS) |

La primera vez que levantes el backend se crean las tablas SQLite y se insertan Waldo's (dictamen vencido) y Sam's Club (aprobado).

## Flujo demo

1. Abrir el mapa → pines en verde/amarillo.
2. Backend y simulador en marcha → se ven los POST en la terminal.
3. Pulsar **W** → Waldo's: corte de luz + temperatura; backend detecta anomalía, cruza Compliance (dictamen vencido), sube severidad, envía WebSocket → pin en rojo y protocolo de emergencia.
4. Pulsar **S** → Sam's Club: gas; mismo flujo, pin en rojo.

## Estructura

- `backend/` — FastAPI, módulos Ingesta, Compliance, Alertas, SQLite.
- `telemetry_simulator/` — Script Python que envía telemetría y atajos W/S.
- `frontend/` — Mapa Leaflet, WebSocket, panel lateral con PC y lecturas.
