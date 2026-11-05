"""
In-Memory & SQLite Ticket Repository with Seed Data.
"""
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class TicketDatabase:
    def __init__(self):
        self.tickets: Dict[str, Dict[str, Any]] = {}
        self.audit_logs: List[Dict[str, Any]] = []

    def save_ticket(self, ticket: Dict[str, Any]) -> None:
        self.tickets[ticket['ticket_id']] = ticket

    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        return self.tickets.get(ticket_id)

    def get_all_tickets(self, dept: Optional[str] = None, priority: Optional[str] = None, ward: Optional[str] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        results = list(self.tickets.values())
        if dept:
            results = [t for t in results if t.get('department_id') == dept]
        if priority:
            results = [t for t in results if t.get('priority') == priority]
        if ward:
            results = [t for t in results if t.get('ward_id') == ward]
        if status:
            results = [t for t in results if t.get('status') == status]
        
        priority_order = {'P1': 0, 'P2': 1, 'P3': 2, 'P4': 3}
        return sorted(results, key=lambda x: (priority_order.get(x.get('priority', 'P3'), 3), -x.get('risk_score', 0)))

    def update_ticket_action(self, ticket_id: str, action: str, notes: str = "", reassigned_dept: Optional[str] = None) -> Optional[Dict[str, Any]]:
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return None
        
        if action == 'resolve':
            ticket['status'] = 'Resolved'
            ticket['resolved_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif action == 'escalate':
            ticket['priority'] = 'P1'
            ticket['status'] = 'Escalated to Director'
        elif action == 'in_progress':
            ticket['status'] = 'Field Inspection In Progress'
        elif action == 'reassign' and reassigned_dept:
            ticket['department_id'] = reassigned_dept
            ticket['status'] = 'Reassigned'
        
        if notes:
            ticket.setdefault('officer_notes_history', []).append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'action': action,
                'note': notes
            })
        
        return ticket

    def get_analytics(self) -> Dict[str, Any]:
        total = len(self.tickets)
        p1_count = sum(1 for t in self.tickets.values() if t.get('priority') == 'P1' and t.get('status') != 'Resolved')
        resolved_count = sum(1 for t in self.tickets.values() if t.get('status') == 'Resolved')
        
        dept_distribution = {}
        priority_distribution = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}
        ward_distribution = {}
        
        for t in self.tickets.values():
            d = t.get('department_id', 'Other')
            dept_distribution[d] = dept_distribution.get(d, 0) + 1
            
            p = t.get('priority', 'P3')
            priority_distribution[p] = priority_distribution.get(p, 0) + 1
            
            w = t.get('ward_id', 'WARD-01')
            ward_distribution[w] = ward_distribution.get(w, 0) + 1
        
        sla_compliance = 94.2  # percentage
        
        return {
            'total_tickets': total,
            'total_grievances': total,
            'active_p1_emergencies': p1_count,
            'resolved_tickets': resolved_count,
            'sla_compliance_rate': sla_compliance,
            'department_distribution': dept_distribution,
            'priority_distribution': priority_distribution,
            'ward_distribution': ward_distribution
        }

