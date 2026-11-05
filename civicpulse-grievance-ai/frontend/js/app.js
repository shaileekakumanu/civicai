/**
 * CivicPulse AI - Ultra-Interactive Citizen Portal Frontend Logic.
 */

const DOMAIN_SUBFEATURES = {
    WOMEN_SAFETY: {
        title: "Women Safety & Protection Squad",
        chips: [
            { label: "Harassment in public places", text: "Group of men passing lewd remarks and harassing women near bus stop in the evening" },
            { label: "Unsafe streets & dark alleys", text: "Complete darkness in residential lane, streetlights not working and feeling unsafe walking" },
            { label: "Stalking & suspicious persons", text: "Suspicious individual following women walking home from metro station for past 3 days" },
            { label: "Eve teasing & verbal abuse", text: "Severe eve teasing and vulgar catcalling outside college gate during evening hours" },
            { label: "Poor lighting near bus stops", text: "Broken high-mast lighting and darkness near Gargi college bus stop creating severe hazard" },
            { label: "Unsafe public transport spots", text: "Shared auto stand with rowdy drunk crowds intimidating women passengers" },
            { label: "Emergency SOS complaint", text: "URGENT SOS: Being stalked by unknown man in dark street in Sector 14, need immediate police patrol" }
        ]
    },
    CHILD_SAFETY: {
        title: "Child Protection & School Safety",
        chips: [
            { label: "Unsafe school zones", text: "Heavy speeding trucks and no zebra crossing or speed breaker outside primary school gate" },
            { label: "Child labour reports", text: "Commercial roadside dhabas and teastalls employing children under 12 years for hazardous cleaning" },
            { label: "Missing child alert", text: "EMERGENCY: 7-year-old missing near Central Market playground since 45 minutes, wearing blue shirt" },
            { label: "Harassment near schools", text: "Suspicious individuals loitering near Girls Senior Secondary School gate intimidating students" },
            { label: "Open drains near schools", text: "Deep open drainage pit right adjacent to school boundary wall, small children at risk of falling" }
        ]
    },
    SENIOR_CITIZEN: {
        title: "Senior Citizen Welfare & Support",
        chips: [
            { label: "Medical emergency support", text: "85-year-old bedridden senior citizen living alone in need of urgent medical welfare assistance" },
            { label: "Abandoned elderly reports", text: "Frail elderly grandmother abandoned on temple pavement without shelter in cold weather" },
            { label: "Unsafe walking paths", text: "Broken and dug-up pavement tiles in park walking track causing multiple senior citizen fall injuries" },
            { label: "Need municipal assistance", text: "Elderly citizen unable to visit office for pension verification, requesting door-to-door visit" }
        ]
    },
    PUBLIC_SAFETY: {
        title: "Public Safety Hazards",
        chips: [
            { label: "Open manholes", text: "Deep uncovered sewer manhole in middle of pedestrian road without barricade or warning" },
            { label: "Live electric wires", text: "High voltage electrical wire snapped and hanging low over public street sparking heavily" },
            { label: "Dangerous construction", text: "5-storey construction without safety nets dropping debris and bricks onto passing pedestrians" },
            { label: "Fallen trees", text: "Massive cracked tree branch leaning dangerously over main road ready to collapse on traffic" },
            { label: "Fire risk", text: "Huge illegal flammable plastic and chemical scrap dump near residential homes" },
            { label: "Street violence", text: "Uncontrolled gang violence and rowdy brawls on market street causing public panic" }
        ]
    },
    HEALTH_HYGIENE: {
        title: "Health, Food Safety & Sanitation",
        chips: [
            { label: "Disease outbreak signs", text: "Multiple cases of viral cholera and severe diarrhea in neighbourhood from community tap" },
            { label: "Mosquito breeding", text: "Stagnant black water pools in open plot breeding dengue mosquitoes, urgent fogging needed" },
            { label: "Contaminated water", text: "Yellow muddy foul-smelling contaminated water flowing from drinking water supply taps" },
            { label: "Food safety complaints", text: "Local restaurant serving stale unhygienic adulterated food causing mass food poisoning" },
            { label: "Garbage causing illness", text: "Uncollected rotten garbage rotting on street for 10 days emitting foul stench and sickness" }
        ]
    },
    ANIMAL_SAFETY: {
        title: "Animal Welfare & Veterinary",
        chips: [
            { label: "Stray dog attacks", text: "Pack of ferocious stray dogs attacking pedestrians and two-wheeler riders, multiple dog bites" },
            { label: "Injured animals", text: "Stray cow hit by speeding vehicle with bleeding leg lying on road, urgent vet rescue needed" },
            { label: "Animal cruelty", text: "Individual brutally beating and starving street animals in colony backyard" },
            { label: "Dead animal removal", text: "Dead dog carcass lying decaying on public pavement causing severe biohazard" }
        ]
    },
    DISABILITY_ACCESS: {
        title: "Disability Accessibility",
        chips: [
            { label: "Broken ramps", text: "Wheelchair ramp at municipal dispensary broken and blocked by cement blocks" },
            { label: "Footpaths blocked", text: "Complete pedestrian sidewalk encroached by illegal shops forcing wheelchair users onto road" },
            { label: "No wheelchair access", text: "Public community hall has steep stairs with zero ramp access for differently-abled citizens" },
            { label: "Unsafe crossings", text: "Metro station pedestrian crossing has no tactile tiles or auditory signals for visually impaired" }
        ]
    },
    ENVIRONMENT: {
        title: "Environmental Protection",
        chips: [
            { label: "Air pollution", text: "Industrial unit releasing thick toxic black chemical smoke and burning plastic in night" },
            { label: "Noise pollution", text: "High decibel DJ and loudspeakers blaring beyond midnight in silent residential zone" },
            { label: "Illegal tree cutting", text: "Commercial contractor illegally felling 10 healthy old green trees without permission" },
            { label: "Lake pollution", text: "Commercial tankers dumping untreated sewage and toxic dye effluent into city lake" },
            { label: "Industrial waste dumping", text: "Chemical factory dumping hazardous sludge on open roadside ground" }
        ]
    },
    DISASTER_EMERGENCY: {
        title: "Disaster Management & Rescue",
        chips: [
            { label: "Flooding & waterlogging", text: "Severe urban flooding with 3 feet water entering ground floor homes and transformer submerged" },
            { label: "Fire breakout", text: "Massive fire erupting in commercial building with trapped persons, urgent fire tender needed" },
            { label: "Building collapse risk", text: "Old multi-storey building showing major structural wall cracks and tilting dangerously" },
            { label: "Storm damage", text: "Violent gale storm uprooted multiple electricity poles and flattened road barriers" },
            { label: "Road blockage", text: "Major landslide and fallen concrete blocks completely blocking highway transit" }
        ]
    },
    CORRUPTION_VIGILANCE: {
        title: "Vigilance & Anti-Corruption",
        chips: [
            { label: "Bribe demand", text: "Municipal official demanding cash bribe to issue property tax receipt and trade license" },
            { label: "Officer not responding", text: "Zonal officer refusing to take complaint and completely neglecting statutory duties" },
            { label: "Fake closure of complaint", text: "Grievance CP-2026-1024 falsely marked as Resolved on portal without performing any repair" },
            { label: "Delayed service without reason", text: "Sanctioned water connection file kept pending for 6 months without any official justification" }
        ]
    }
};

const WARD_LOCATIONS = {
    'WARD-01': { name: 'Ward 01 - Central Market', lat: 28.6315, lng: 77.2167 },
    'WARD-02': { name: 'Ward 02 - Civil Lines', lat: 28.6750, lng: 77.2250 },
    'WARD-03': { name: 'Ward 03 - Green Park', lat: 28.5589, lng: 77.2028 },
    'WARD-04': { name: 'Ward 04 - Lajpat Nagar', lat: 28.5684, lng: 77.2435 },
    'WARD-05': { name: 'Ward 05 - Indiranagar', lat: 28.6010, lng: 77.2910 },
    'WARD-06': { name: 'Ward 06 - Model Town', lat: 28.7020, lng: 77.1930 },
    'WARD-07': { name: 'Ward 07 - Sector 21', lat: 28.5820, lng: 77.0600 },
    'WARD-08': { name: 'Ward 08 - Koramangala', lat: 28.5350, lng: 77.2600 }
};

let debounceTimer = null;
let miniMap = null;
let pinMarker = null;
let isRecording = false;
let speechRecognizer = null;

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    selectDomain('WOMEN_SAFETY');
    initMiniMap();
    setupEventListeners();
    setupPhotoDropzone();
});

function initMiniMap() {
    const mapEl = document.getElementById('miniMap');
    if (!mapEl) return;

    miniMap = L.map('miniMap', { zoomControl: false }).setView([28.62, 77.21], 11);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(miniMap);

    // Click on map to drop pin and find closest ward
    miniMap.on('click', (e) => {
        const { lat, lng } = e.latlng;
        setPinLocation(lat, lng);
    });
}

function setPinLocation(lat, lng) {
    if (pinMarker) miniMap.removeLayer(pinMarker);

    pinMarker = L.marker([lat, lng]).addTo(miniMap);
    document.getElementById('pinCoordText').textContent = `GPS: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;

    // Auto-detect closest ward
    let closestWard = 'WARD-01';
    let minDistance = Infinity;

    for (const [wId, info] of Object.entries(WARD_LOCATIONS)) {
        const d = Math.hypot(info.lat - lat, info.lng - lng);
        if (d < minDistance) {
            minDistance = d;
            closestWard = wId;
        }
    }

    const select = document.getElementById('wardSelect');
    select.value = closestWard;
    showToast(`📍 Ward Auto-Detected: ${WARD_LOCATIONS[closestWard].name}`, 'info');
    triggerLiveAnalysis();
}

function selectDomain(domainKey) {
    const data = DOMAIN_SUBFEATURES[domainKey];
    if (!data) return;

    // Highlight selected card
    document.querySelectorAll('.domain-card').forEach(c => {
        c.classList.remove('ring-2', 'ring-sky-500', 'bg-sky-50');
    });
    const activeCard = document.getElementById(`card-${domainKey}`);
    if (activeCard) activeCard.classList.add('ring-2', 'ring-sky-500', 'bg-sky-50');
    
    document.getElementById('subfeatureDomainTitle').textContent = `${data.title} Sub-Categories:`;
    const container = document.getElementById('subfeatureChips');
    container.innerHTML = '';

    data.chips.forEach(chip => {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'px-3 py-1.5 rounded-lg bg-white border border-slate-300 hover:border-sky-500 hover:text-sky-700 text-xs font-medium transition shadow-sm flex items-center space-x-1.5 text-slate-700 hover:scale-105';
        btn.innerHTML = `<span>⚡</span><span>${chip.label}</span>`;
        btn.onclick = () => {
            const textarea = document.getElementById('grievanceText');
            textarea.value = chip.text;
            textarea.focus();
            showToast(`Loaded Template: ${chip.label}`, 'info');
            triggerLiveAnalysis();
        };
        container.appendChild(btn);
    });
}

function triggerEmergencySOS() {
    selectDomain('WOMEN_SAFETY');
    const textarea = document.getElementById('grievanceText');
    textarea.value = "EMERGENCY SOS: In immediate danger, being harassed and followed near bus stop in Sector 14. Requesting instant Women Safety Police Patrol dispatch!";
    textarea.focus();
    showToast("🚨 Emergency SOS Triggered!", "error");
    triggerLiveAnalysis();
}

function setDistressEmoji(type) {
    document.querySelectorAll('.emoji-btn').forEach(b => b.classList.remove('bg-slate-200'));
    const textarea = document.getElementById('grievanceText');
    let current = textarea.value.trim();

    if (type === 'rage') {
        textarea.value = current ? current + " This is completely unacceptable and outrageous!" : "Severe life safety hazard and outrageous negligence.";
    } else if (type === 'fear') {
        textarea.value = current ? current + " Feeling extremely terrified and unsafe." : "Terrified for public safety, urgent help needed.";
    } else if (type === 'worried') {
        textarea.value = current ? current + " Causing severe distress and suffering for days." : "Severely distressed by ongoing failure.";
    }
    textarea.focus();
    triggerLiveAnalysis();
}

function setupEventListeners() {
    const textarea = document.getElementById('grievanceText');
    const wardSelect = document.getElementById('wardSelect');
    const form = document.getElementById('grievanceForm');
    const trackBtn = document.getElementById('trackBtn');
    const voiceBtn = document.getElementById('voiceBtn');
    const slider = document.getElementById('urgencySlider');

    if (textarea) {
        textarea.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(triggerLiveAnalysis, 300);
        });
    }

    if (wardSelect) {
        wardSelect.addEventListener('change', () => {
            const w = wardSelect.value;
            if (w && WARD_LOCATIONS[w] && miniMap) {
                miniMap.setView([WARD_LOCATIONS[w].lat, WARD_LOCATIONS[w].lng], 13);
                if (pinMarker) miniMap.removeLayer(pinMarker);
                pinMarker = L.marker([WARD_LOCATIONS[w].lat, WARD_LOCATIONS[w].lng]).addTo(miniMap);
            }
            triggerLiveAnalysis();
        });
    }

    if (form) form.addEventListener('submit', handleGrievanceSubmit);
    if (trackBtn) trackBtn.addEventListener('click', handleTrackGrievance);
    if (voiceBtn) voiceBtn.addEventListener('click', toggleVoiceDictation);

    if (slider) {
        slider.addEventListener('input', (e) => {
            const val = parseInt(e.target.value);
            const labels = { 1: "P4 (Routine Servicing)", 2: "P3 (Standard 48h)", 3: "P2 (High Priority 12h)", 4: "P1 (Critical Emergency 2h)" };
            document.getElementById('sliderUrgencyLabel').textContent = labels[val];
            triggerLiveAnalysis();
        });
    }
}

function toggleVoiceDictation() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const wave = document.getElementById('recordingWave');
    const btn = document.getElementById('voiceBtn');
    const btnText = document.getElementById('voiceBtnText');

    if (!SpeechRecognition) {
        // Fallback simulation
        simulateVoiceInput();
        return;
    }

    if (isRecording) {
        if (speechRecognizer) speechRecognizer.stop();
        isRecording = false;
        wave.classList.add('hidden');
        btn.classList.remove('mic-recording');
        btnText.textContent = "Voice Dictation";
        showToast("Mic recording stopped", "info");
        return;
    }

    speechRecognizer = new SpeechRecognition();
    speechRecognizer.lang = 'en-IN';
    speechRecognizer.continuous = false;
    speechRecognizer.interimResults = true;

    speechRecognizer.onstart = () => {
        isRecording = true;
        wave.classList.remove('hidden');
        btn.classList.add('mic-recording');
        btnText.textContent = "Listening...";
        showToast("🎙️ Microphone Active - Speak your grievance", "info");
    };

    speechRecognizer.onresult = (e) => {
        const transcript = Array.from(e.results).map(r => r[0].transcript).join('');
        const textarea = document.getElementById('grievanceText');
        textarea.value = transcript;
        triggerLiveAnalysis();
    };

    speechRecognizer.onerror = (e) => {
        console.warn("Speech recognition error:", e);
        isRecording = false;
        wave.classList.add('hidden');
        btn.classList.remove('mic-recording');
        btnText.textContent = "Voice Dictation";
        simulateVoiceInput();
    };

    speechRecognizer.onend = () => {
        isRecording = false;
        wave.classList.add('hidden');
        btn.classList.remove('mic-recording');
        btnText.textContent = "Voice Dictation";
    };

    speechRecognizer.start();
}

function simulateVoiceInput() {
    const samples = [
        "Ladkiyon ko chedte hain bus stop pe Lajpat Nagar me, andhera hai aur koi police patrol nahi hai",
        "Large open manhole right outside DAV Public School gate in Sector 14, small children at extreme risk",
        "82-year-old paralyzed elderly citizen living alone in Sector 21 requires emergency medical support",
        "High voltage live electric wire snapped and sparking on road near school in Sector 14",
        "Municipal building inspector demanding 50000 cash bribe to approve building sanction in Ward 02",
        "Wheelchair ramp at municipal dispensary broken, disabled citizens unable to enter building",
        "Factory in industrial area releasing dense toxic chemical smoke causing breathing choking in night"
    ];
    const chosen = samples[Math.floor(Math.random() * samples.length)];
    const textarea = document.getElementById('grievanceText');
    textarea.value = chosen;
    textarea.focus();
    showToast("🎙️ Voice Dictation Transcript Generated", "info");
    triggerLiveAnalysis();
}

function setupPhotoDropzone() {
    const dropzone = document.getElementById('dropzone');
    const photoInput = document.getElementById('photoInput');

    if (!dropzone || !photoInput) return;

    dropzone.addEventListener('click', () => photoInput.click());
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files.length) handlePhotoFile(e.dataTransfer.files[0]);
    });

    photoInput.addEventListener('change', (e) => {
        if (e.target.files.length) handlePhotoFile(e.target.files[0]);
    });
}

function handlePhotoFile(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('previewImgName').textContent = file.name;
        document.getElementById('dropzonePrompt').classList.add('hidden');
        document.getElementById('dropzonePreview').classList.remove('hidden');
        showToast("📷 Photo Uploaded: AI Computer Vision Hazard Verified", "success");
    };
    reader.readAsDataURL(file);
}

function removePhoto() {
    document.getElementById('photoInput').value = '';
    document.getElementById('previewImg').src = '';
    document.getElementById('dropzonePrompt').classList.remove('hidden');
    document.getElementById('dropzonePreview').classList.add('hidden');
}

async function triggerLiveAnalysis() {
    const text = document.getElementById('grievanceText').value.trim();
    const ward = document.getElementById('wardSelect').value;
    const previewCard = document.getElementById('aiPreviewCard');

    if (!text || text.length < 5) {
        if (previewCard) previewCard.classList.add('hidden');
        return;
    }

    try {
        const res = await fetch('/api/grievance/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, ward_id: ward || null })
        });

        if (!res.ok) return;
        const data = await res.json();
        renderLiveAIPreview(data);
    } catch (err) {
        console.error("Live analysis failed:", err);
    }
}

function renderLiveAIPreview(data) {
    const previewCard = document.getElementById('aiPreviewCard');
    if (!previewCard) return;

    previewCard.classList.remove('hidden');

    // Priority badge
    const prioEl = document.getElementById('previewPriority');
    prioEl.textContent = `${data.priority} Priority`;
    prioEl.className = `px-2.5 py-0.5 rounded-full text-xs font-bold badge-${data.priority.toLowerCase()}`;

    // Risk Meter
    document.getElementById('previewRiskScore').textContent = `${data.risk_score} / 100`;
    const bar = document.getElementById('previewRiskBar');
    bar.style.width = `${data.risk_score}%`;
    bar.className = `h-full transition-all duration-300 ${data.risk_score >= 80 ? 'bg-red-600' : data.risk_score >= 60 ? 'bg-orange-500' : 'bg-amber-500'}`;

    // Details Grid
    document.getElementById('previewDept').textContent = data.department_name;
    document.getElementById('previewSubcat').textContent = data.subcategory || "General Inspection";
    document.getElementById('previewHelpline').textContent = data.helpline || "112 / 100";
    document.getElementById('previewSLA').textContent = `${data.sla_hours} Hours Response`;
    document.getElementById('previewWard').textContent = data.ward_name || "Ward 01";
    document.getElementById('previewLang').textContent = data.normalization?.detected_language || "English";

    // XAI Tokens
    const xaiContainer = document.getElementById('previewXAI');
    xaiContainer.innerHTML = '';
    if (data.xai && data.xai.token_attributions) {
        data.xai.token_attributions.forEach(tok => {
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

    document.getElementById('previewRationale').textContent = data.xai?.decision_rationale || "";
}

async function handleGrievanceSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.innerHTML = `<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> Processing AI Dispatch...`;

    const text = document.getElementById('grievanceText').value.trim();
    const name = document.getElementById('citizenName').value.trim() || "Concerned Citizen";
    const phone = document.getElementById('citizenPhone').value.trim() || "+91 98765-00000";
    const ward = document.getElementById('wardSelect').value || null;

    try {
        const res = await fetch('/api/grievance/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text,
                citizen_name: name,
                citizen_phone: phone,
                ward_id: ward
            })
        });

        if (!res.ok) throw new Error("Submission failed");
        const ticket = await res.json();

        // Populate Success Modal
        document.getElementById('modalTicketId').textContent = ticket.ticket_id;
        document.getElementById('modalDept').textContent = ticket.department_name;
        document.getElementById('modalPriority').textContent = `${ticket.priority} (${ticket.sla_hours}h SLA)`;
        document.getElementById('modalWorkOrder').textContent = ticket.work_order?.work_order_no || "WO-DISPATCH-001";
        document.getElementById('modalSMS').textContent = ticket.citizen_notification?.sms_english || "Dispatched successfully.";

        // Incident Cluster Alert
        const clusterAlert = document.getElementById('modalClusterAlert');
        if (ticket.cluster_info && !ticket.cluster_info.is_new_cluster) {
            clusterAlert.classList.remove('hidden');
            document.getElementById('modalClusterCount').textContent = ticket.cluster_info.affected_citizens_count;
        } else {
            clusterAlert.classList.add('hidden');
        }

        document.getElementById('successModal').classList.remove('hidden');
        document.getElementById('grievanceForm').reset();
        document.getElementById('aiPreviewCard').classList.add('hidden');
        removePhoto();
        showToast("🎉 Grievance Dispatched & Work Order Created!", "success");
        lucide.createIcons();

    } catch (err) {
        showToast("Submission error: " + err.message, "error");
    } finally {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="send" class="w-4 h-4"></i> Submit Grievance Now`;
        lucide.createIcons();
    }
}

async function handleTrackGrievance() {
    const ticketId = document.getElementById('trackInput').value.trim();
    if (!ticketId) {
        showToast("Please enter a Ticket ID.", "error");
        return;
    }

    try {
        const res = await fetch(`/api/grievance/track/${ticketId}`);
        if (!res.ok) {
            showToast("Ticket not found. Please verify the ID.", "error");
            return;
        }

        const data = await res.json();
        document.getElementById('trackTitle').textContent = `Ticket: ${data.ticket_id}`;
        document.getElementById('trackSummary').textContent = data.raw_text;
        document.getElementById('trackStatus').textContent = data.status;
        document.getElementById('trackDept').textContent = data.department_name;
        document.getElementById('trackPriority').textContent = `${data.priority} (Target SLA: ${data.sla_hours}h)`;
        document.getElementById('trackDeadline').textContent = data.work_order?.sla_deadline_iso || "Immediate";

        document.getElementById('trackModal').classList.remove('hidden');
    } catch (err) {
        showToast("Error tracking ticket: " + err.message, "error");
    }
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
