/**
 * IGNIS Frontend - Map and pins.
 * Hermosillo center: 29.0729, -110.9559
 */
const HERMOSILLO = [29.0729, -110.9559];

let map = null;
let markers = {};
let branchState = {}; // branch_id -> 'normal' | 'warning' | 'alert'

function getPinColor(state) {
  switch (state) {
    case "alert": return "pin-alert";
    case "warning": return "pin-warning";
    default: return "pin-normal";
  }
}

function createIcon(state) {
  const className = getPinColor(state);
  return L.divIcon({
    className: "custom-pin " + className,
    html: `<div class="${className}" style="width:24px;height:24px;border-radius:50%;"></div>`,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });
}

async function loadSucursales() {
  const res = await fetch(`${window.API_BASE}/sucursales`);
  if (!res.ok) throw new Error("No se pudieron cargar sucursales");
  return res.json();
}

function openPanel(sucursalId) {
  if (window.showDashboard) window.showDashboard(sucursalId);
  const panel = document.getElementById("panel");
  panel.classList.remove("closed");
}

function addMarker(sucursal) {
  const id = sucursal.id;
  branchState[id] = "normal";
  const latlng = [sucursal.lat, sucursal.lng];
  const marker = L.marker(latlng, {
    icon: createIcon("normal"),
  }).addTo(map);
  marker.bindPopup(`<b>${sucursal.nombre}</b><br/>Riesgo base: ${sucursal.nivel_riesgo_base}`, {
    autoPan: false,
  });
  marker.on("click", () => openPanel(id));
  marker.sucursal = sucursal;
  markers[id] = marker;
}

function setPinState(branchId, state) {
  branchState[branchId] = state;
  const marker = markers[branchId];
  if (!marker) return;
  var el = marker.getElement();
  if (el) {
    var pinClass = getPinColor(state);
    el.className = "custom-pin leaflet-marker-icon leaflet-interactive " + pinClass;
    var inner = el.querySelector("div");
    if (inner) inner.className = pinClass;
  }
}

function showEmergencyToast(message) {
  const el = document.getElementById("emergency-toast");
  el.textContent = message;
  el.classList.remove("hidden");
  setTimeout(() => el.classList.add("hidden"), 8000);
}

// Expose for websocket and dashboard
window.setPinState = setPinState;
window.showEmergencyToast = showEmergencyToast;
window.markers = () => markers;
window.branchState = () => branchState;

async function init() {
  const mapEl = document.getElementById("map");
  if (!mapEl) return;
  mapEl.style.height = "100%";
  mapEl.style.minHeight = "300px";

  map = L.map("map").setView(HERMOSILLO, 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
  }).addTo(map);

  setTimeout(function () {
    if (map) map.invalidateSize();
  }, 100);

  try {
    const sucursales = await loadSucursales();
    sucursales.forEach(addMarker);
  } catch (e) {
    console.error(e);
    var statusEl = document.getElementById("ws-status");
    if (statusEl) statusEl.textContent = "Error cargando sucursales. ¿Backend en marcha?";
  }
}

document.addEventListener("DOMContentLoaded", init);
