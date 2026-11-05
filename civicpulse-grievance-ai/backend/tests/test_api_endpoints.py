"""
Integration Tests for CivicPulse FastAPI Endpoints across 10 Domains.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_and_static():
    response = client.get("/")
    assert response.status_code == 200
    assert "CivicPulse AI" in response.text
    print("[PASS] Root & Citizen Portal HTML Serving")

def test_analyze_endpoint():
    payload = {
        "text": "Men are drinking and eve teasing women near bus stop in Sector 14",
        "ward_id": None
    }
    res = client.post("/api/grievance/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["department_id"] == "WOMEN_SAFETY"
    assert data["priority"] == "P1"
    assert "1091" in data["helpline"]
    assert data["ward_id"] == "WARD-02"
    print("[PASS] /api/grievance/analyze 10-Domain Live AI Triage")

def test_submit_and_track_endpoint():
    payload = {
        "text": "Deep open manhole outside DAV Public School in Sector 14",
        "citizen_name": "Test Citizen",
        "citizen_phone": "+91 9876543210",
        "ward_id": "WARD-02"
    }
    res = client.post("/api/grievance/submit", json=payload)
    assert res.status_code == 200
    ticket = res.json()
    ticket_id = ticket["ticket_id"]
    assert ticket_id.startswith("CP-2026-")
    assert ticket["department_id"] == "CHILD_SAFETY"
    print(f"[PASS] /api/grievance/submit (Created Ticket {ticket_id})")

    # Track
    track_res = client.get(f"/api/grievance/track/{ticket_id}")
    assert track_res.status_code == 200
    track_data = track_res.json()
    assert track_data["ticket_id"] == ticket_id
    print(f"[PASS] /api/grievance/track/{ticket_id}")

def test_admin_endpoints():
    # Tickets
    res = client.get("/api/admin/tickets")
    assert res.status_code == 200
    tickets = res.json()["tickets"]
    assert len(tickets) > 0
    print(f"[PASS] /api/admin/tickets ({len(tickets)} tickets retrieved)")

    # Analytics
    ana_res = client.get("/api/admin/analytics")
    assert ana_res.status_code == 200
    ana = ana_res.json()
    assert ana["total_tickets"] > 0
    print("[PASS] /api/admin/analytics")

    # Batch Benchmark across 10 domains
    bench_res = client.get("/api/admin/batch-benchmark")
    assert bench_res.status_code == 200
    bench = bench_res.json()
    assert bench["accuracy_percent"] >= 95.0
    print(f"[PASS] /api/admin/batch-benchmark (Accuracy: {bench['accuracy_percent']:.1f}%)")

if __name__ == '__main__':
    test_root_and_static()
    test_analyze_endpoint()
    test_submit_and_track_endpoint()
    test_admin_endpoints()
    print("\n=== All Integration Tests Passed Successfully! ===")
