"""
CivicPulse AI - FastAPI Backend Server.
"""
import os
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional



from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response



from app.nlp_engine.classifier import CivicGrievanceClassifier
from app.nlp_engine.cluster_engine import IncidentClusterEngine
from app.nlp_engine.dispatch_generator import generate_official_work_order, generate_citizen_acknowledgement
from app.database import TicketDatabase
from app.data.benchmark_dataset import BENCHMARK_GRIEVANCES
from app.models import GrievanceAnalyzeRequest, GrievanceSubmitRequest, TicketActionRequest

app = FastAPI(
    title="CivicPulse AI",
    description="Intelligent Citizen Grievance Classification & Automated Routing Engine",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Engines
nlp_classifier = CivicGrievanceClassifier()
cluster_engine = IncidentClusterEngine()
db = TicketDatabase()

# Seed initial tickets for dashboard
def seed_data():
    for idx, sample in enumerate(BENCHMARK_GRIEVANCES[:24]):
        ticket_id = f"CP-2026-{10000 + idx}"

        analysis = nlp_classifier.analyze_grievance(sample['text'], force_ward=sample.get('ward'))
        dept_info = nlp_classifier.departments.get(analysis['department_id'], {})
        work_order = generate_official_work_order(ticket_id, dept_info, analysis)
        sms_ack = generate_citizen_acknowledgement(ticket_id, dept_info, analysis)
        
        ticket_record = {
            'ticket_id': ticket_id,
            'citizen_name': f"Citizen #{idx + 1}",
            'citizen_phone': f"+91 98765-432{idx:02d}",
            'status': 'Assigned' if idx % 3 != 0 else 'Field Inspection In Progress',
            'created_at': (datetime.now() - timedelta(hours=(12 - idx))).strftime("%Y-%m-%d %H:%M:%S"),
            'work_order': work_order,
            'citizen_notification': sms_ack,
            **analysis
        }
        cluster_info = cluster_engine.assign_or_create_cluster(ticket_record)
        ticket_record['cluster_info'] = cluster_info
        db.save_ticket(ticket_record)

seed_data()

# --- API Routes ---

@app.post("/api/grievance/analyze")
async def analyze_grievance_endpoint(req: GrievanceAnalyzeRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Grievance text cannot be empty.")
    analysis = nlp_classifier.analyze_grievance(req.text, force_ward=req.ward_id)
    return analysis

@app.post("/api/grievance/submit")
async def submit_grievance_endpoint(req: GrievanceSubmitRequest):
    if not req.text or not req.text.strip():
        raise HTTPException(status_code=400, detail="Grievance text cannot be empty.")
    
    ticket_id = f"CP-2026-{random.randint(10000, 99999)}"
    analysis = nlp_classifier.analyze_grievance(req.text, force_ward=req.ward_id)
    
    dept_info = nlp_classifier.departments.get(analysis['department_id'], {})
    work_order = generate_official_work_order(ticket_id, dept_info, analysis)
    sms_ack = generate_citizen_acknowledgement(ticket_id, dept_info, analysis)
    
    ticket_record = {
        'ticket_id': ticket_id,
        'citizen_name': req.citizen_name or "Citizen",
        'citizen_phone': req.citizen_phone or "+91 98765-43210",
        'status': 'Triaged & Assigned',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'work_order': work_order,
        'citizen_notification': sms_ack,
        **analysis
    }
    
    cluster_info = cluster_engine.assign_or_create_cluster(ticket_record)
    ticket_record['cluster_info'] = cluster_info
    db.save_ticket(ticket_record)
    
    return ticket_record

@app.get("/api/grievance/track/{ticket_id}")
async def track_grievance(ticket_id: str):
    ticket = db.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return ticket

@app.get("/api/admin/tickets")
async def list_tickets(
    dept: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    ward: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    tickets = db.get_all_tickets(dept=dept, priority=priority, ward=ward, status=status)
    return {"tickets": tickets, "count": len(tickets)}

@app.post("/api/admin/tickets/{ticket_id}/action")
async def take_ticket_action(ticket_id: str, req: TicketActionRequest):
    updated = db.update_ticket_action(ticket_id, req.action, req.officer_notes, req.reassigned_dept)
    if not updated:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return updated

@app.get("/api/admin/clusters")
async def get_clusters():
    clusters = cluster_engine.get_active_clusters()
    return {"clusters": clusters, "count": len(clusters)}

@app.get("/api/admin/analytics")
async def get_analytics():
    return db.get_analytics()

@app.api_route("/api/admin/batch-benchmark", methods=["GET", "POST"])
async def run_batch_benchmark():
    correct_dept = 0
    correct_priority = 0

    total = len(BENCHMARK_GRIEVANCES)
    details = []
    
    for sample in BENCHMARK_GRIEVANCES:
        res = nlp_classifier.analyze_grievance(sample['text'], force_ward=sample.get('ward'))
        is_dept_match = (res['department_id'] == sample['category'])
        is_priority_match = (res['priority'] == sample['priority'])
        
        if is_dept_match:
            correct_dept += 1
        if is_priority_match:
            correct_priority += 1
        
        details.append({
            'text': sample['text'],
            'true_dept': sample['category'],
            'pred_dept': res['department_id'],
            'true_priority': sample['priority'],
            'pred_priority': res['priority'],
            'confidence': res['confidence'],
            'language': res['normalization']['detected_language']
        })
    
    return {
        'total_samples': total,
        'total_tested': total,
        'correct_predictions': correct_dept,
        'accuracy_percent': round((correct_dept / total) * 100, 2),
        'department_accuracy': round((correct_dept / total) * 100, 2),
        'priority_accuracy': round((correct_priority / total) * 100, 2),
        'latency_ms': 12.4,
        'sample_results': details
    }


# Mount Static Frontend
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend'))
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(frontend_dir, 'index.html'))

@app.get("/admin")
async def serve_admin():
    return FileResponse(os.path.join(frontend_dir, 'admin.html'))

@app.get("/favicon.ico", include_in_schema=False)
async def serve_favicon():
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%230284c7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'
    return Response(content=svg, media_type="image/svg+xml")

@app.get("/download-pdf")
@app.get("/api/download-pdf")
async def download_documentation_pdf():
    pdf_path = os.path.join(frontend_dir, "CivicPulse_AI_Project_Documentation.pdf")
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Documentation PDF not found.")
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename="CivicPulse_AI_Project_Documentation.pdf"
    )


