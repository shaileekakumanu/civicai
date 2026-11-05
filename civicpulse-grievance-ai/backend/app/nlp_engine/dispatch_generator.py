"""
Automated Dual Dispatch & Notification Synthesizer.
Generates Official Municipal Work Orders & Citizen SMS/WhatsApp Acknowledgments.
"""
from datetime import datetime, timedelta
from typing import Dict, Any

def generate_official_work_order(ticket_id: str, dept_info: Dict[str, Any], grievance_data: Dict[str, Any]) -> Dict[str, Any]:
    sla_hours = grievance_data.get("sla_hours", 24)
    created_at = datetime.now()
    sla_deadline = created_at + timedelta(hours=sla_hours)
    
    work_order = {
        "work_order_no": f"WO-{dept_info.get('short_code', 'MUN')}-{ticket_id[-6:]}",
        "ticket_ref": ticket_id,
        "issuing_authority": dept_info.get("name", "Municipal Corporation"),
        "assigned_officer": dept_info.get("nodal_officer", "Zonal Field Engineer"),
        "priority_level": grievance_data.get("priority", "P3"),
        "category": grievance_data.get("category_name", "Civic Works"),
        "subcategory": grievance_data.get("subcategory", "General Inspection"),
        "ward_location": grievance_data.get("ward_name", "Ward 1"),
        "incident_summary": grievance_data.get("summary", "Citizen report requiring inspection."),
        "sla_deadline_iso": sla_deadline.strftime("%Y-%m-%d %H:%M:%S"),
        "sla_hours_allocated": sla_hours,
        "field_action_checklist": [
            "Dispatch rapid response inspection crew with field gear",
            "Verify on-site hazard extent & coordinate with local Ward supervisor",
            "Execute corrective repair / remediation & upload geo-tagged resolution photo",
            "Obtain citizen digital sign-off and close service ticket in CRM"
        ]
    }
    return work_order

def generate_citizen_acknowledgement(ticket_id: str, dept_info: Dict[str, Any], grievance_data: Dict[str, Any]) -> Dict[str, str]:
    dept_name = dept_info.get("name", "Municipal Department")
    priority = grievance_data.get("priority", "P3")
    sla_h = grievance_data.get("sla_hours", 24)
    cat_name = grievance_data.get('category_name', 'Civic Issue')
    
    sms_en = (
        f"[CivicPulse Alert] Grievance #{ticket_id} received. Category: {cat_name}. "
        f"Routed to {dept_name}. Priority: {priority} (Target SLA: {sla_h}h). "
        f"Track real-time status: https://civicpulse.gov.in/track/{ticket_id}"
    )
    
    sms_hi = (
        f"[Nagrik Sewa] Aapki Shikayat #{ticket_id} darj ho gayi hai. "
        f"Vibhag: {dept_name}. Priority: {priority} (Time: {sla_h} ghante). "
        f"Status track karen: https://civicpulse.gov.in/track/{ticket_id}"
    )
    
    return {
        "sms_english": sms_en,
        "sms_hindi": sms_hi,
        "tracking_url": f"https://civicpulse.gov.in/track/{ticket_id}"
    }
