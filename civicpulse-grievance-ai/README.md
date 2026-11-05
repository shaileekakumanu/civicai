# 🏛️ CivicPulse AI: Intelligent Citizen Grievance Classification & Automated Routing Platform

An end-to-end, novel Natural Language Processing (NLP) system designed to solve the critical urban governance challenge of triaging, prioritizing, and dispatching unstructured citizen grievances across municipal departments.

---

## 🌟 Problem & Research Gaps Addressed

### 1. The Core Problem
Municipal governance systems receive thousands of complaints daily across Water Works, Electricity, Roads/Traffic, Solid Waste, Drainage, Public Health, Law & Order, and Horticulture. Manually reading, assessing urgency, identifying location landmarks, and routing complaints to the correct nodal officer causes severe delays in resolving critical public issues.

### 2. Research Gaps in Existing Systems
| Existing Civic Triage Systems | **CivicPulse AI Innovation** |
| :--- | :--- |
| **Only generic text classification** (ignores urgency priority) | **Hierarchical Multi-Aspect NLP + Safety Heuristic Overrides (P1-P4)** with automated SLA calculation. |
| **Monolingual English only** (fails on Indian code-mixed Hinglish) | **Civic Vernacular Normalizer** mapping 150+ romanized Hindi terms and phrases to semantic concepts. |
| **Isolated complaint handling** (duplicate spam & storm spikes) | **Unsupervised TF-IDF Cosine Incident Deduplication & Clustering** that aggregates spikes into Master Incidents. |
| **Black-box predictions** | **Explainable AI (XAI)** token-level attribution & distress sentiment scoring explaining why an issue was prioritized. |
| **Manual dispatch process** | **Dual Dispatch Generator**: Instant Municipal Work Orders with rapid checklists + Bilingual Citizen SMS/WhatsApp. |

---

## 🏗️ System Architecture

```
                                  [ Citizen Input ]
                        (English / Code-Mixed Hinglish / Audio)
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │   Hinglish & Vernacular Normalizer    │
                     │  (Transliteration & Lexicon Mapping)  │
                     └───────────────────┬───────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌────────────────────────────────┐       ┌────────────────────────────────┐
   │    Civic-NER Entity Engine     │       │ Hierarchical Multi-Task Model  │
   │ (Wards, Assets, Durations, LMs)│       │ (Dept, Subcategory, Urgency)   │
   └────────────────┬───────────────┘       └────────────────┬───────────────┘
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         │
                                         ▼
                     ┌───────────────────────────────────────┐
                     │  XAI Explainer & Distress Analyzer   │
                     │  (Token Attributions & Risk Scoring)  │
                     └───────────────────┬───────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌────────────────────────────────┐       ┌────────────────────────────────┐
   │  Incident Deduplication Engine │       │    Dual Dispatch Generator     │
   │ (Spike Detection & Clustering) │       │ (Work Order & Bilingual SMS)   │
   └────────────────┬───────────────┘       └────────────────┬───────────────┘
                    │                                         │
                    └────────────────────┬────────────────────┘
                                         ▼
                     ┌───────────────────────────────────────┐
                     │       FastAPI High-Speed Server       │
                     └───────────────────┬───────────────────┘
                                         │
                    ┌────────────────────┴────────────────────┐
                    ▼                                         ▼
   ┌────────────────────────────────┐       ┌────────────────────────────────┐
   │    Citizen Grievance Portal    │       │   Municipal Command Center     │
   │  (Live Triage Preview & Voice) │       │  (GIS Map, Queues & Analytics) │
   └────────────────────────────────┘       └────────────────────────────────┘
```

---

## ⚡ Key Features

1. **Hierarchical NLP Classifier**:
   - 8 Major Municipal Departments & 25+ Sub-categories.
   - Dynamic 4-Tier Urgency Matrix:
     - **P1 - Critical Emergency** (2–6 Hours SLA): Live hanging wires, transformer fire, toxic water contamination, dengue outbreaks.
     - **P2 - High Priority** (12–24 Hours SLA): Water pipeline burst, deep road craters, overflowing sewer manholes.
     - **P3 - Medium Priority** (36–72 Hours SLA): Garbage dumps, non-functional streetlights, overgrown branches.
     - **P4 - Routine Maintenance** (72–168 Hours SLA): Park benches, general inquiries, stray dog neutering requests.

2. **Hinglish & Code-Mixed Normalizer**:
   - Accurately interprets colloquial queries like *"Paani nahi aa raha hai 3 din se Sector 14 me"* or *"Sadak pe bade gaddhe hain gaadi toot gayi"*.

3. **Civic-NER Location Extractor**:
   - Auto-extracts Wards (Wards 1–8), Localities/Sectors, Public Asset IDs (e.g., `Pole #12`, `Transformer TX-4`), and incident durations.

4. **Incident Deduplication & Spike Detection**:
   - Uses TF-IDF cosine similarity across spatial buckets to automatically detect when 5+ citizens report the same transformer blast or pipe burst, merging them into a single Master Incident.

5. **Explainable AI (XAI) & Sentiment Scoring**:
   - Highlights exact tokens that triggered emergency prioritization and provides natural language justifications for auditability.

6. **Interactive Municipal Command Center**:
   - Live Leaflet.js Ward GIS Heatmap.
   - Real-time SLA monitoring and department workload charts.
   - 1-Click batch benchmark evaluator.

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Edge, Firefox)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application (One-Click)
```bash
python run_demo.py
```
This automatically launches the FastAPI server and opens the Citizen Portal at `http://127.0.0.1:8000`.

### 3. Access Portals
- **Citizen Grievance Portal**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Municipal Command Center**: [http://127.0.0.1:8000/static/admin.html](http://127.0.0.1:8000/static/admin.html)
- **Interactive REST API Docs (Swagger)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Run Unit Tests
```bash
python backend/tests/test_nlp_engine.py
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/grievance/analyze` | `POST` | Real-time live AI analysis on typing (Category, Priority, Entities, XAI). |
| `/api/grievance/submit` | `POST` | Lodge a complaint with work order generation and clustering. |
| `/api/grievance/track/{id}`| `GET` | Track ticket status, SLA timer, and dispatch timeline. |
| `/api/admin/tickets` | `GET` | Retrieve and filter triage queues. |
| `/api/admin/tickets/{id}/action` | `POST` | Escalate, assign, in-progress, or resolve grievances. |
| `/api/admin/clusters` | `GET` | Retrieve active incident deduplication spike clusters. |
| `/api/admin/analytics` | `GET` | Aggregate SLA compliance and department workload statistics. |
| `/api/admin/batch-benchmark`| `GET` | Run 1-click batch benchmark across the test dataset. |
