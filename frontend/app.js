// --- API base: use localhost to avoid IPv4/IPv6 mismatches ---
const API = ""; // same-origin (e.g., /assessments, /stats/current)
console.log("app.js v3; API base:", API || "(same-origin)");


// --- Grab elements explicitly (no relying on globals) ---
const els = {
  title: document.getElementById("title"),
  weight: document.getElementById("weight"),
  due: document.getElementById("due"),
  score: document.getElementById("score"),
  addBtn: document.getElementById("add"),
  tableBody: document.querySelector("#table tbody"),
  current: document.getElementById("current"),
  remaining: document.getElementById("remaining"),
  weightsMsg: document.getElementById("weightsMsg"),
  target: document.getElementById("target"),
  calcBtn: document.getElementById("calc"),
  answer: document.getElementById("answer"),
};

// --- Track editing state (Add vs Update) ---
let editingId = null;

function setEditingMode(assessment) {
  editingId = assessment.id;
  els.title.value = assessment.title;
  els.weight.value = assessment.weight_pct;
  els.due.value = assessment.due_date; // API is YYYY-MM-DD
  els.score.value = assessment.score_pct ?? "";
  els.addBtn.textContent = "Update";
  ensureCancelButton();
}

function clearEditingMode() {
  editingId = null;
  els.title.value = "";
  els.weight.value = "";
  els.due.value = "";
  els.score.value = "";
  els.addBtn.textContent = "Add / Update";
  removeCancelButton();
}

function ensureCancelButton() {
  if (document.getElementById("cancel-edit")) return;
  const btn = document.createElement("button");
  btn.id = "cancel-edit";
  btn.type = "button";
  btn.textContent = "Cancel";
  btn.style.marginLeft = ".5rem";
  btn.onclick = clearEditingMode;
  els.addBtn.insertAdjacentElement("afterend", btn);
}

function removeCancelButton() {
  const btn = document.getElementById("cancel-edit");
  if (btn) btn.remove();
}

async function fetchJSON(url, opts = {}) {
  const r = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!r.ok) {
    const msg = await r.text().catch(() => r.statusText);
    throw new Error(`${r.status} ${msg}`);
  }
  return r.status === 204 ? null : r.json();
}


async function load() {
  // List assessments
  const rows = await fetchJSON(`${API}/assessments`);
  els.tableBody.innerHTML = "";
  rows.forEach((r) => {
    const tr = document.createElement("tr");
    tr.setAttribute("data-id", r.id);
    tr.innerHTML = `
      <td>${r.title}</td>
      <td>${r.weight_pct}%</td>
      <td>${r.due_date}</td>
      <td>${(r.score_pct !== null && r.score_pct !== undefined) ? r.score_pct : ""}</td>
      <td>
        <button data-id="${r.id}" class="edit">Edit</button>
        <button data-id="${r.id}" class="del">Delete</button>
      </td>
    `;
    els.tableBody.appendChild(tr);
  });

    // Empty state
  if (rows.length === 0) {
    const tr = document.createElement("tr");
    tr.className = "empty";
    tr.innerHTML = `<td colspan="5">No assessments yet — add your first one above ✨</td>`;
    els.tableBody.appendChild(tr);
  }


  // Stats
  const stats = await fetchJSON(`${API}/stats/current`);
  els.current.textContent = stats.current_weighted.toFixed(2);
  els.remaining.textContent = stats.remaining_weight.toFixed(2);

  // Weight validation
  const v = await fetchJSON(`${API}/stats/validate`);
  els.weightsMsg.textContent = v.message;
}


// Create (Add / Update button)
els.addBtn.onclick = async () => {
  const payload = {
    title: els.title.value.trim(),
    weight_pct: Number(els.weight.value),
    due_date: els.due.value, // YYYY-MM-DD
    score_pct: els.score.value === "" ? null : Number(els.score.value),
  };

  if (!payload.title || !payload.due_date || Number.isNaN(payload.weight_pct)) {
    alert("Please fill Title, Weight and Due Date.");
    return;
  }

  if (editingId == null) {
    await fetchJSON(`${API}/assessments`, {
      method: "POST",
      body: JSON.stringify(payload),
    });
  } else {
    await fetchJSON(`${API}/assessments/${editingId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    });
  }

  await load();
  clearEditingMode();
};


// Delete via event delegation
document.querySelector("#table").onclick = async (e) => {
  if (e.target.classList.contains("del")) {
    const id = e.target.getAttribute("data-id");
    await fetch(`${API}/assessments/${id}`, { method: "DELETE" });
    await load();
  }
};
// Edit via event delegation
document.querySelector("#table").addEventListener("click", async (e) => {
  const btn = e.target.closest("button.edit");
  if (!btn) return;
  const id = Number(btn.dataset.id);
  const a = await fetchJSON(`${API}/assessments/${id}`);
  setEditingMode(a);
});


// What-if
els.calcBtn.onclick = async () => {
  const t = Number(els.target.value);
  if (Number.isNaN(t)) return (els.answer.textContent = "Enter a target %");
  const r = await fetchJSON(`${API}/stats/what-if?target=${t}`);
  els.answer.textContent =
    r.required_avg == null
      ? `No remaining work. Target ${r.target}% is ${r.attainable ? "already met" : "not met"}.`
      : `You need an average of ${r.required_avg}% on remaining work. (${r.attainable ? "attainable" : "not attainable"})`;
};

load();
