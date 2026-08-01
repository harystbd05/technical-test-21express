const API_BASE = "/api/v1/shipments";

const el = {
  body: document.getElementById("shipmentBody"),
  alert: document.getElementById("alertBox"),
  statTotal: document.getElementById("statTotal"),
  statCreated: document.getElementById("statCreated"),
  statDelivered: document.getElementById("statDelivered"),
  statTariff: document.getElementById("statTariff"),
  modal: document.getElementById("createModal"),
  createForm: document.getElementById("createForm"),
};

function showAlert(message, type = "error") {
  el.alert.textContent = message;
  el.alert.hidden = false;
  el.alert.className = type === "success" ? "alert alert--success" : "alert";
  setTimeout(() => {
    el.alert.hidden = true;
  }, 4000);
}

function formatRupiah(amount) {
  return "Rp " + Number(amount).toLocaleString("id-ID");
}

function statusStamp(status) {
  const cls = status === "DELIVERED" ? "stamp--delivered" : "stamp--created";
  return `<span class="stamp ${cls}">${status}</span>`;
}

async function fetchShipments() {
  el.body.innerHTML = `<tr><td colspan="8" class="empty">Memuat data...</td></tr>`;
  try {
    const res = await fetch(API_BASE);
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    renderTable(json.data);
    renderSummary(json.data);
  } catch (err) {
    el.body.innerHTML = `<tr><td colspan="8" class="empty">Gagal memuat data: ${err.message}</td></tr>`;
  }
}

function renderSummary(shipments) {
  const total = shipments.length;
  const created = shipments.filter((s) => s.status === "CREATED").length;
  const delivered = shipments.filter((s) => s.status === "DELIVERED").length;
  const totalTariff = shipments.reduce((sum, s) => sum + s.total_tariff, 0);

  el.statTotal.textContent = total;
  el.statCreated.textContent = created;
  el.statDelivered.textContent = delivered;
  el.statTariff.textContent = formatRupiah(totalTariff);
}

function renderTable(shipments) {
  if (shipments.length === 0) {
    el.body.innerHTML = `<tr><td colspan="8" class="empty">Belum ada resi. Klik "+ Buat Resi" untuk mulai.</td></tr>`;
    return;
  }

  el.body.innerHTML = shipments
    .map(
      (s) => `
    <tr>
      <td class="mono">#${s.id}</td>
      <td>${escapeHtml(s.item_name)}</td>
      <td class="mono">${s.piece}</td>
      <td class="mono">${s.weight}</td>
      <td class="mono">${s.service_code}</td>
      <td class="mono">${formatRupiah(s.total_tariff)}</td>
      <td>${statusStamp(s.status)}</td>
      <td class="actions">
        ${
          s.status === "CREATED"
            ? `<button class="btn btn--primary btn--sm" onclick="markDelivered(${s.id})">Set Delivered</button>`
            : ""
        }
        <button class="btn btn--danger btn--sm" onclick="removeShipment(${s.id})">Hapus</button>
      </td>
    </tr>
  `,
    )
    .join("");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

async function markDelivered(id) {
  try {
    const res = await fetch(`${API_BASE}/${id}/status`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: "DELIVERED" }),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    showAlert("Status resi diperbarui menjadi DELIVERED", "success");
    fetchShipments();
  } catch (err) {
    showAlert(err.message);
  }
}

async function removeShipment(id) {
  if (!confirm(`Hapus resi #${id}? Tindakan ini tidak bisa dibatalkan.`))
    return;
  try {
    const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    showAlert("Resi berhasil dihapus", "success");
    fetchShipments();
  } catch (err) {
    showAlert(err.message);
  }
}

el.createForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(el.createForm);
  const payload = {
    item_name: formData.get("item_name"),
    piece: parseInt(formData.get("piece"), 10),
    weight: parseFloat(formData.get("weight")),
    service_code: formData.get("service_code"),
  };

  try {
    const res = await fetch(API_BASE, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const json = await res.json();
    if (!json.success) throw new Error(json.message);
    showAlert("Resi baru berhasil dibuat", "success");
    el.createForm.reset();
    toggleModal(false);
    fetchShipments();
  } catch (err) {
    showAlert(err.message);
  }
});

function toggleModal(show) {
  el.modal.hidden = !show;
}

document
  .getElementById("openCreateBtn")
  .addEventListener("click", () => toggleModal(true));
document
  .getElementById("closeCreateBtn")
  .addEventListener("click", () => toggleModal(false));
document.getElementById("refreshBtn").addEventListener("click", fetchShipments);
el.modal.addEventListener("click", (e) => {
  if (e.target === el.modal) toggleModal(false);
});

fetchShipments();
