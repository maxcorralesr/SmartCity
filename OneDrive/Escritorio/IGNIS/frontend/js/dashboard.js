/**
 * Panel lateral: detalle de sucursal, compliance, última lectura, alerta activa.
 */
let selectedSucursalId = null;
let chartTemp = null;
let chartPower = null;

const panel = document.getElementById("panel");
const panelClose = document.getElementById("panel-close");
const panelTitle = document.getElementById("panel-title");
const panelCompliance = document.getElementById("panel-compliance");
const panelLastReading = document.getElementById("panel-last-reading");
const panelAlert = document.getElementById("panel-alert");

if (panelClose) {
  panelClose.addEventListener("click", () => {
    panel.classList.add("closed");
  });
}

async function fetchSucursalDetail(id) {
  const res = await fetch(`${window.API_BASE}/sucursales/${id}`);
  if (!res.ok) return null;
  return res.json();
}

async function fetchTelemetryBuffer(id) {
  const res = await fetch(`${window.API_BASE}/telemetry/buffer/${id}`);
  if (!res.ok) return [];
  return res.json();
}

function renderCompliance(auditorias) {
  if (!auditorias || auditorias.length === 0) {
    return "<div class=\"estado\">Sin datos de auditoría</div>";
  }
  const last = auditorias[auditorias.length - 1];
  const isAprobado = last.estado === "Aprobado";
  return `
    <h3>Protección Civil</h3>
    <div class="estado ${isAprobado ? "aprobado" : "vencido"}">${last.estado}</div>
    <p style="margin-top:0.5rem;font-size:0.8rem;color:#8b98a5;">Último dictamen: ${last.fecha_ultimo_dictamen}</p>
  `;
}

function renderLastReading(data) {
  if (!data || data.length === 0) return "Sin lecturas recientes.";
  const last = data[data.length - 1];
  return `
    <p>Temperatura: <strong>${last.temperature} °C</strong></p>
    <p>Voltaje: <strong>${last.voltage} V</strong> · Amperaje: <strong>${last.amperage} A</strong></p>
    <p style="font-size:0.8rem;color:#8b98a5;">${new Date(last.timestamp).toLocaleTimeString()}</p>
  `;
}

function updateCharts(buffer) {
  if (!buffer || buffer.length < 2 || typeof Chart === "undefined") return;
  const labels = buffer.map((b) => new Date(b.timestamp).toLocaleTimeString("es", { minute: "2-digit", second: "2-digit" }));
  const tempData = buffer.map((b) => b.temperature);
  const voltageData = buffer.map((b) => b.voltage);

  const tempEl = document.getElementById("chart-temp");
  const powerEl = document.getElementById("chart-power");
  if (tempEl) {
    if (chartTemp) chartTemp.destroy();
    chartTemp = new Chart(tempEl, {
      type: "line",
      data: { labels, datasets: [{ label: "Temperatura °C", data: tempData, borderColor: "#00ba7c", tension: 0.3 }] },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: false } } },
    });
  }
  if (powerEl) {
    if (chartPower) chartPower.destroy();
    chartPower = new Chart(powerEl, {
      type: "line",
      data: { labels, datasets: [{ label: "Voltaje V", data: voltageData, borderColor: "#ffad00", tension: 0.3 }] },
      options: { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } },
    });
  }
}

function showDashboard(sucursalId) {
  selectedSucursalId = sucursalId;
  panel.classList.remove("closed");
  panelTitle.textContent = "Cargando…";
  panelCompliance.innerHTML = "";
  panelLastReading.innerHTML = "";
  panelAlert.classList.add("hidden");

  (async () => {
    const sucursal = await fetchSucursalDetail(sucursalId);
    if (!sucursal) {
      panelTitle.textContent = "Sucursal no encontrada";
      return;
    }
    panelTitle.textContent = sucursal.nombre;
    panelCompliance.innerHTML = renderCompliance(sucursal.auditorias_pc);

    const buffer = await fetchTelemetryBuffer(sucursalId);
    panelLastReading.innerHTML =
      "<h3>Última lectura</h3>" +
      renderLastReading(buffer) +
      "<div class=\"chart-container\"><canvas id=\"chart-temp\"></canvas></div>" +
      "<div class=\"chart-container\"><canvas id=\"chart-power\"></canvas></div>";
    updateCharts(buffer);
  })();
}

window.showDashboard = showDashboard;

window.onAlertMessage = function (msg) {
  if (msg.sucursal_id === selectedSucursalId && panelAlert) {
    panelAlert.classList.remove("hidden");
    panelAlert.innerHTML = `
      <h3>Protocolo de emergencia</h3>
      <div class="protocolo">${msg.protocolo || ""}</div>
    `;
  }
};
