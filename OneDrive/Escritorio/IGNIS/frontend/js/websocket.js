/**
 * WebSocket client for real-time alerts.
 * Shared config for all scripts (loaded first).
 */
window.API_BASE = window.API_BASE || "http://localhost:8000/api";
const WS_URL = "ws://localhost:8000/ws";
let ws = null;
let reconnectTimer = null;

function updateStatus(className, text) {
  const el = document.getElementById("ws-status");
  if (!el) return;
  el.className = "ws-status " + className;
  el.textContent = text;
}

function connect() {
  ws = new WebSocket(WS_URL);
  ws.onopen = () => updateStatus("connected", "Conectado en vivo");
  ws.onclose = () => {
    updateStatus("error", "Desconectado. Reconectando…");
    reconnectTimer = setTimeout(connect, 3000);
  };
  ws.onerror = () => updateStatus("error", "Error de conexión");
  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.sucursal_id != null && window.setPinState) {
        window.setPinState(msg.sucursal_id, "alert");
      }
      if (msg.protocolo && window.showEmergencyToast) {
        window.showEmergencyToast("ALERTA: " + (msg.tipo || "Incidente") + " – " + msg.protocolo);
      }
      if (window.onAlertMessage) window.onAlertMessage(msg);
    } catch (e) {
      console.error("WS message parse error", e);
    }
  };
}

connect();

window.wsConnection = { connect, close: () => { if (ws) ws.close(); } };
