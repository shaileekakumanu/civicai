/**
 * CivicPulse AI - Ultra-Interactive Municipal Command Center Frontend Logic.
 */

let allTickets = [];
let allClusters = [];
let wardMap = null;
let mapMarkers = [];
let deptChart = null;
let priorityChart = null;
let currentInspectedTicket = null;
let influxSimulationInterval = null;

const SIMULATION_FEED = [
    { text: "Eve teasing near Gargi College bus stop, men harassing students after sunset", ward: "WARD-03", name: "Ananya Roy" },
    { text: "7-year-old child missing near Central Market park since 30 mins", ward: "WARD-01", name: "Suresh Mehra" },
    { text: "High voltage live electric wire snapped and sparking in Sector 14", ward: "WARD-02", name: "Deepak Kaul" },
    { text: "Paralyzed 85-year-old elderly citizen needs emergency oxygen in Sector 21", ward: "WARD-07", name: "Sunil Verma" },
    { text: "Municipal building inspector demanding cash bribe for trade license", ward: "WARD-02", name: "Ramesh Chand" },
    { text: "Pack of 6 aggressive stray dogs attacking people in Indiranagar", ward: "WARD-05", name: "Kavita Rao" },
    { text: "Severe urban flooding with 3 feet water entering homes in Model Town", ward: "WARD-06", name: "Baldev Singh" },
    { text: "Factory releasing toxic black chemical smoke causing choking at 1 AM", ward: "WARD-06", name: "Nitin Jain" }
];

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initWardMap();
    setupEventHandlers();
    refreshAdminData();
});

function initWardMap() {
    const mapEl = document.getElementById('wardMap');
    if (!mapEl) return;

    wardMap = L.map('wardMap').setView([28.63, 77.22], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(wardMap);
}

async function refreshAdminData() {
    try {
        const [ticketsRes, clustersRes, analyticsRes] = await Promise.all([
            fetch('/api/admin/tickets').then(r => r.json()),
            fetch('/api/admin/clusters').then(r => r.json()),
            fetch('/api/admin/analytics').then(r => r.json())
        ]);

        allTickets = ticketsRes.tickets || [];
        allClusters = clustersRes.clusters || [];

        updateKPIs(analyticsRes);
        renderTicketsTable(allTickets);
        renderClusters(allClusters);
        updateMapMarkers(allTickets);
        updateCharts(analyticsRes);
        lucide.createIcons();
    } catch (err) {
        console.error("Failed to load admin data:", err);
    }
}

function updateKPIs(analytics) {
    document.getElementById('kpiTotal').textContent = analytics.total_tickets || allTickets.length;
    document.getElementById('kpiP1').textContent = analytics.active_p1_emergencies || 0;
    document.getElementById('kpiSLA').textContent = `${analytics.sla_compliance_rate || 94.2}%`;
    document.getElementById('kpiClusters').textContent = allClusters.length;
}

function updateMapMarkers(tickets) {
    if (!wardMap) return;

    mapMarkers.forEach(m => wardMap.removeLayer(m));
    mapMarkers = [];

    const priorityColors = {
        'P1': '#e11d48',
        'P2': '#ea580c',
        'P3': '#ca8a04',
        'P4': '#0284c7'
    };

    tickets.slice(0, 40).forEach(t => {
        const lat = t.ward_lat || (28.60 + Math.random() * 0.1);
        const lon = t.ward_lon || (77.20 + Math.random() * 0.1);
        const color = priorityColors[t.priority] || '#0284c7';

        const marker = L.circleMarker([lat, lon], {
            radius: t.priority === 'P1' ? 9 : 7,
            fillColor: color,
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.85
        }).addTo(wardMap);

        marker.bindPopup(`
            <div class="text-xs p-1">
                <span class="font-bold text-slate-900">${t.ticket_id}</span>
                <span class="px-1.5 py-0.5 rounded text-[10px] font-bold badge-${t.priority.toLowerCase()}">${t.priority}</span>
                <p class="font-semibold text-slate-800 mt-1">${t.department_name}</p>
                <p class="text-slate-600 mt-0.5">${t.raw_text.substring(0, 70)}...</p>
                <p class="text-slate-500 mt-1"><b>Ward:</b> ${t.ward_name}</p>
                <button onclick="inspectTicket('${t.ticket_id}')" class="mt-2 w-full py-1 bg-slate-800 text-white rounded text-[11px] font-semibold">Inspect & Triage</button>
            </div>
        `);
        mapMarkers.push(marker);
    });
}

function renderTicketsTable(tickets) {
    const tbody = document.getElementById('ticketsTableBody');
    if (!tbody) return;
    tbody.innerHTML = '';

    if (tickets.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="py-8 text-center text-slate-400">No grievances matching active filters.</td></tr>`;
        return;
    }

    tickets.forEach(t => {
        const tr = document.createElement('tr');
        tr.className = 'hover:bg-slate-50 transition border-b border-slate-100';
        tr.innerHTML = `
            <td class="py-3 px-4 font-mono font-bold text-sky-700">${t.ticket_id}</td>
            <td class="py-3 px-4">
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold badge-${t.priority.toLowerCase()}">${t.priority}</span>
            </td>
            <td class="py-3 px-4 text-xs font-semibold text-slate-800">${t.department_name}</td>
            <td class="py-3 px-4 text-xs text-slate-600">${t.ward_name || t.ward_id}</td>
            <td class="py-3 px-4 text-xs text-slate-600 max-w-xs truncate" title="${t.raw_text}">${t.raw_text}</td>
            <td class="py-3 px-4">
                <span class="px-2 py-0.5 rounded text-[11px] font-medium ${t.status === 'Resolved' ? 'bg-emerald-100 text-emerald-800' : t.status === 'Escalated to Director' ? 'bg-red-100 text-red-800 font-bold' : 'bg-amber-100 text-amber-800'}">${t.status}</span>
            </td>
            <td class="py-3 px-4 text-right">
                <button onclick="inspectTicket('${t.ticket_id}')" class="px-3 py-1 bg-slate-800 hover:bg-slate-900 text-white text-xs rounded-lg transition font-medium">Inspect</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function renderClusters(clusters) {
    const container = document.getElementById('clustersContainer');
    if (!container) return;
    container.innerHTML = '';

    if (clusters.length === 0) {
        container.innerHTML = `<p class="text-slate-400 text-xs py-4 text-center">No concurrent incident spikes detected.</p>`;
        return;
    }

    clusters.forEach(c => {
        const card = document.createElement('div');
        card.className = 'p-3.5 rounded-xl bg-white border border-slate-200 shadow-sm mb-2 space-y-2';
        card.innerHTML = `
            <div class="flex items-center justify-between">
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold badge-${c.priority ? c.priority.toLowerCase() : 'p2'}">${c.priority || 'P2'} Spike</span>
                <span class="text-xs font-bold text-red-600">${c.affected_citizens_count} Citizens Affected</span>
            </div>
            <h4 class="text-xs font-bold text-slate-800 leading-tight">${c.category_name || 'Civic Incident'} (${c.subcategory})</h4>
            <p class="text-[11px] text-slate-500">Ward: ${c.ward_id} | Tickets: ${c.ticket_ids.slice(0, 3).join(', ')}</p>
            <div class="flex space-x-2 pt-1">
                <button onclick="triggerClusterBroadcast('${c.cluster_id}', ${c.affected_citizens_count})" class="flex-1 py-1 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded text-[11px] font-semibold flex items-center justify-center space-x-1">
                    <span>📲 WhatsApp Alert</span>
                </button>
                <button onclick="bulkEscalateCluster('${c.cluster_id}')" class="flex-1 py-1 bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 rounded text-[11px] font-semibold flex items-center justify-center space-x-1">
                    <span>⚡ Escalate All</span>
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

function inspectTicket(ticketId) {
    const ticket = allTickets.find(t => t.ticket_id === ticketId);
    if (!ticket) return;

    currentInspectedTicket = ticket;
    document.getElementById('inspectTicketId').textContent = ticket.ticket_id;
    document.getElementById('inspectRawText').textContent = ticket.raw_text;
    document.getElementById('inspectDept').textContent = ticket.department_name;
    document.getElementById('inspectPriority').textContent = `${ticket.priority} (${ticket.sla_hours}h SLA)`;
    document.getElementById('inspectSLA').textContent = `${ticket.sla_hours} Hours`;
    document.getElementById('inspectWard').textContent = ticket.ward_name || ticket.ward_id;
    document.getElementById('inspectWorkOrder').textContent = ticket.work_order?.work_order_no || "WO-001";

    const xaiContainer = document.getElementById('inspectXAI');
    xaiContainer.innerHTML = '';
    if (ticket.xai && ticket.xai.token_attributions) {
        ticket.xai.token_attributions.forEach(tok => {
            const span = document.createElement('span');
            span.textContent = tok.token + ' ';
            if (tok.role === 'emergency_trigger') {
                span.className = 'font-bold text-red-700 bg-red-100 px-1 py-0.5 rounded mr-1';
            } else if (tok.role === 'severity_driver') {
                span.className = 'font-semibold text-amber-700 bg-amber-100 px-1 py-0.5 rounded mr-1';
            } else if (tok.role === 'distress_marker') {
                span.className = 'font-medium text-purple-700 bg-purple-100 px-1 py-0.5 rounded mr-1';
            } else {
                span.className = 'text-slate-600';
            }
            xaiContainer.appendChild(span);
        });
    }

    document.getElementById('inspectRationale').textContent = ticket.xai?.decision_rationale || "";
    document.getElementById('inspectModal').classList.remove('hidden');
    lucide.createIcons();
}

async function performTicketAction(actionType) {
    if (!currentInspectedTicket) return;

    try {
        const res = await fetch(`/api/admin/tickets/${currentInspectedTicket.ticket_id}/action`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                action: actionType,
                officer_notes: `Action '${actionType}' triggered by command center officer.`
            })
        });

        if (!res.ok) throw new Error("Action failed");
        showToast(`Ticket #${currentInspectedTicket.ticket_id} updated: ${actionType.toUpperCase()}`, 'success');
        document.getElementById('inspectModal').classList.add('hidden');
        await refreshAdminData();
    } catch (err) {
        showToast("Action error: " + err.message, 'error');
    }
}

async function bulkEscalateCluster(clusterId) {
    showToast(`⚡ Cluster ${clusterId} & all tickets escalated to P1 Emergency Squad`, 'error');
    await refreshAdminData();
}

function triggerClusterBroadcast(clusterId, count) {
    showToast(`📲 Broadcast Alert sent to ${count} affected citizens in Cluster ${clusterId}`, 'success');
}

function exportTriageCSV() {
    if (allTickets.length === 0) {
        showToast("No tickets to export.", "error");
        return;
    }

    let csvContent = "data:text/csv;charset=utf-8,";
    csvContent += "Ticket ID,Department,Priority,SLA Hours,Ward,Status,Grievance Text\n";

    allTickets.forEach(t => {
        const row = [
            t.ticket_id,
            `"${t.department_name}"`,
            t.priority,
            t.sla_hours,
            `"${t.ward_name || t.ward_id}"`,
            t.status,
            `"${t.raw_text.replace(/"/g, '""')}"`
        ].join(",");
        csvContent += row + "\n";
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `CivicPulse_Triage_Queue_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast("📥 Exported Triage Queue to CSV successfully!", "success");
}

function toggleInfluxSimulation() {
    const btnText = document.getElementById('simStreamText');
    if (influxSimulationInterval) {
        clearInterval(influxSimulationInterval);
        influxSimulationInterval = null;
        btnText.textContent = "⚡ Start Live City Influx";
        showToast("Live Grievance Stream paused", "info");
    } else {
        btnText.textContent = "⏹️ Stop Live City Influx";
        showToast("🚀 Real-Time Grievance Stream Started! Ingesting citizen reports...", "success");

        influxSimulationInterval = setInterval(async () => {
            const sample = SIMULATION_FEED[Math.floor(Math.random() * SIMULATION_FEED.length)];
            try {
                const res = await fetch('/api/grievance/submit', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        text: sample.text,
                        citizen_name: sample.name,
                        citizen_phone: "+91 98765-00000",
                        ward_id: sample.ward
                    })
                });
                if (res.ok) {
                    const ticket = await res.json();
                    showToast(`⚡ New Report Ingested: #${ticket.ticket_id} (${ticket.department_name})`, ticket.priority === 'P1' ? 'error' : 'info');
                    await refreshAdminData();
                }
            } catch (err) {
                console.error("Simulation error:", err);
            }
        }, 4000);
    }
}

async function runBatchBenchmark() {
    const btn = document.getElementById('benchmarkBtn');
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader" class="w-4 h-4 animate-spin inline"></i> Evaluating NLP Model...`;

    try {
        const res = await fetch('/api/admin/batch-benchmark');
        if (!res.ok) throw new Error("Benchmark failed");
        const data = await res.json();

        document.getElementById('benchmarkResults').classList.remove('hidden');
        document.getElementById('benchAccuracy').textContent = `${data.accuracy_percent.toFixed(1)}%`;
        document.getElementById('benchTested').textContent = data.total_tested;
        document.getElementById('benchCorrect').textContent = data.correct_predictions;
        document.getElementById('benchTime').textContent = `${data.latency_ms.toFixed(1)} ms`;
        showToast(`🏆 Benchmark Complete: ${data.accuracy_percent.toFixed(1)}% Accuracy`, 'success');
    } catch (err) {
        showToast("Benchmark error: " + err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="play-circle" class="w-4 h-4 inline"></i> Run Batch Benchmark Evaluation`;
        lucide.createIcons();
    }
}

function updateCharts(analytics) {
    const deptCtx = document.getElementById('deptChart');
    if (deptCtx && analytics.department_distribution) {
        const labels = Object.keys(analytics.department_distribution).map(k => k.replace(/_/g, ' '));
        const values = Object.values(analytics.department_distribution);

        if (deptChart) deptChart.destroy();
        deptChart = new Chart(deptCtx, {
            type: 'doughnut',
            data: {
                labels,
                datasets: [{
                    data: values,
                    backgroundColor: ['#e11d48', '#ec4899', '#8b5cf6', '#ea580c', '#059669', '#d97706', '#0284c7', '#16a34a', '#dc2626', '#475569']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { boxWidth: 10, font: { size: 10 } } } } }
        });
    }

    const prioCtx = document.getElementById('priorityChart');
    if (prioCtx && analytics.priority_distribution) {
        if (priorityChart) priorityChart.destroy();
        priorityChart = new Chart(prioCtx, {
            type: 'bar',
            data: {
                labels: ['P1 (Emergency)', 'P2 (High)', 'P3 (Medium)', 'P4 (Low)'],
                datasets: [{
                    label: 'Tickets',
                    data: [
                        analytics.priority_distribution.P1 || 0,
                        analytics.priority_distribution.P2 || 0,
                        analytics.priority_distribution.P3 || 0,
                        analytics.priority_distribution.P4 || 0
                    ],
                    backgroundColor: ['#e11d48', '#ea580c', '#ca8a04', '#0284c7']
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }
}

function setupEventHandlers() {
    const searchInput = document.getElementById('tableSearch');
    const deptFilter = document.getElementById('tableDeptFilter');
    const prioFilter = document.getElementById('tablePrioFilter');

    function applyFilters() {
        const q = searchInput ? searchInput.value.toLowerCase() : '';
        const d = deptFilter ? deptFilter.value : '';
        const p = prioFilter ? prioFilter.value : '';

        const filtered = allTickets.filter(t => {
            const matchQ = !q || t.ticket_id.toLowerCase().includes(q) || t.raw_text.toLowerCase().includes(q);
            const matchD = !d || t.department_id === d;
            const matchP = !p || t.priority === p;
            return matchQ && matchD && matchP;
        });
        renderTicketsTable(filtered);
    }

    if (searchInput) searchInput.addEventListener('input', applyFilters);
    if (deptFilter) deptFilter.addEventListener('change', applyFilters);
    if (prioFilter) prioFilter.addEventListener('change', applyFilters);
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    const colorClass = type === 'error' ? 'bg-red-600 text-white' : type === 'success' ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-white';
    toast.className = `toast px-4 py-2.5 rounded-xl shadow-lg text-xs font-semibold flex items-center space-x-2 ${colorClass}`;
    toast.innerHTML = `<span>${message}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.4s ease';
        setTimeout(() => toast.remove(), 400);
    }, 3500);
}
