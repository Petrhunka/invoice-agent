"""
Standalone script to generate sample CSV data
Run this before first use if data files don't exist
"""

import csv
import random
from datetime import datetime, timedelta

def generate_invoice_requests():
    """Generate 30 sample pending requests"""
    
    vendors = [
        "Acme Corp", "TechGlobal Solutions", "MegaSoft Industries", 
        "DataFlow Systems", "CloudVentures Inc", "NextGen Technologies",
        "Prime Logistics", "Elite Manufacturing", "Global Trade Partners",
        "Innovative Solutions", "Strategic Services", "Precision Engineering",
        "Digital Dynamics", "Enterprise Solutions", "Alpha Industries"
    ]
    
    reasons = [
        "Cash flow constraints due to delayed client payments",
        "Unexpected operational expenses this quarter",
        "Temporary supply chain disruption affecting liquidity",
        "Seasonal revenue fluctuation impacting payment capacity",
        "Recent equipment investment affecting short-term cash position",
        "Client payment delays causing temporary cash shortage",
        "End of fiscal year budget reconciliation needed",
        "Restructuring payment schedules to align with revenue cycles"
    ]
    
    requests = []
    base_date = datetime.now()
    
    # Set seed for reproducibility
    random.seed(42)
    
    for i in range(1, 31):
        vendor = random.choice(vendors)
        
        # Generate amount with varied distribution
        amount_category = random.choice(['low', 'medium', 'high'])
        if amount_category == 'low':
            amount = random.uniform(3000, 15000)
        elif amount_category == 'medium':
            amount = random.uniform(15000, 35000)
        else:
            amount = random.uniform(35000, 67000)
        
        due_date = base_date + timedelta(days=random.randint(2, 60))
        extension_days = random.choice([7, 14, 21, 30])
        priority = random.choices(['High', 'Medium', 'Low'], weights=[0.25, 0.45, 0.30])[0]
        vendor_reliability = random.uniform(0.70, 0.95)
        payment_history = random.uniform(0.75, 0.94)
        cash_flow = random.choices(['Low', 'Medium', 'High'], weights=[0.30, 0.45, 0.25])[0]
        submission_date = base_date - timedelta(days=random.randint(1, 10))
        
        requests.append({
            'request_id': f'REQ-{1000 + i}',
            'vendor_name': vendor,
            'invoice_amount': round(amount, 2),
            'original_due_date': due_date.strftime('%Y-%m-%d'),
            'requested_extension_days': extension_days,
            'reason': random.choice(reasons),
            'priority': priority,
            'vendor_reliability_score': round(vendor_reliability, 2),
            'payment_history_score': round(payment_history, 2),
            'cash_flow_impact': cash_flow,
            'submission_date': submission_date.strftime('%Y-%m-%d')
        })
    
    # Write to CSV
    with open('data/invoice_requests.csv', 'w', newline='') as f:
        fieldnames = [
            'request_id', 'vendor_name', 'invoice_amount', 'original_due_date',
            'requested_extension_days', 'reason', 'priority', 'vendor_reliability_score',
            'payment_history_score', 'cash_flow_impact', 'submission_date'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(requests)
    
    print(f"✅ Generated {len(requests)} invoice requests")


def generate_decisions():
    """Generate 50 sample historical decisions"""
    
    vendors = [
        "Acme Corp", "TechGlobal Solutions", "MegaSoft Industries", 
        "DataFlow Systems", "CloudVentures Inc", "NextGen Technologies",
        "Prime Logistics", "Elite Manufacturing", "Global Trade Partners",
        "Innovative Solutions", "Strategic Services", "Precision Engineering"
    ]
    
    decisions = []
    base_date = datetime.now()
    
    random.seed(43)
    
    # Generate distribution: 72% approved, 12% rejected, 16% escalated
    decision_types = ['Approved'] * 36 + ['Rejected'] * 6 + ['Approved'] * 8
    random.shuffle(decision_types)
    
    for i in range(1, 51):
        decision_date = base_date - timedelta(
            days=random.randint(1, 60),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        ai_decision = decision_types[i-1] if i <= len(decision_types) else 'Approved'
        final_decision = ai_decision
        
        # Higher confidence for approved, lower for rejected
        if ai_decision == 'Approved':
            confidence = random.uniform(0.70, 0.94)
        else:
            confidence = random.uniform(0.45, 0.75)
        
        amount = random.uniform(5000, 55000)
        processing_time = random.uniform(30, 300)
        
        decisions.append({
            'request_id': f'REQ-{900 + i}',
            'decision_date': decision_date.strftime('%Y-%m-%d %H:%M:%S'),
            'ai_decision': ai_decision,
            'confidence_score': round(confidence, 2),
            'human_review': random.choices([True, False], weights=[0.15, 0.85])[0],
            'final_decision': final_decision,
            'processing_time_seconds': round(processing_time, 1),
            'vendor_name': random.choice(vendors),
            'invoice_amount': round(amount, 2)
        })
    
    # Write to CSV
    with open('data/decisions.csv', 'w', newline='') as f:
        fieldnames = [
            'request_id', 'decision_date', 'ai_decision', 'confidence_score',
            'human_review', 'final_decision', 'processing_time_seconds',
            'vendor_name', 'invoice_amount'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(decisions)
    
    print(f"✅ Generated {len(decisions)} decisions")


def generate_audit_log():
    """Generate sample audit log entries"""
    
    actions = [
        "Decision: Approved", "Decision: Rejected", "Export: CSV", 
        "View: Dashboard", "View: Reports", "Login", "Data Refresh"
    ]
    
    users = ["Current User", "System Admin", "Finance Manager"]
    
    logs = []
    base_date = datetime.now()
    
    random.seed(44)
    
    for i in range(25):
        timestamp = base_date - timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        action = random.choice(actions)
        request_id = f'REQ-{random.randint(900, 1030)}' if 'Decision' in action else 'N/A'
        
        if 'Approved' in action:
            details = 'Email sent to vendor, payment extension granted'
        elif 'Rejected' in action:
            details = 'Email sent to vendor, request denied'
        elif 'Export' in action:
            details = 'Downloaded decision history report'
        else:
            details = f'User accessed {action.split(": ")[1] if ": " in action else "system"}'
        
        logs.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'action': action,
            'user': random.choice(users),
            'request_id': request_id,
            'details': details,
            'ip_address': f'192.168.1.{random.randint(1, 255)}'
        })
    
    # Sort by timestamp descending
    logs.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Write to CSV
    with open('data/audit_log.csv', 'w', newline='') as f:
        fieldnames = ['timestamp', 'action', 'user', 'request_id', 'details', 'ip_address']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)
    
    print(f"✅ Generated {len(logs)} audit log entries")


if __name__ == "__main__":
    print("Generating sample data...")
    print("=" * 50)
    
    generate_invoice_requests()
    generate_decisions()
    generate_audit_log()
    
    print("=" * 50)
    print("✅ All sample data generated successfully!")
    print("\nFiles created:")
    print("  - data/invoice_requests.csv (30 records)")
    print("  - data/decisions.csv (50 records)")
    print("  - data/audit_log.csv (25 records)")

