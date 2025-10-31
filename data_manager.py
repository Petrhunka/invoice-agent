"""
Data Manager for Invoice Payment Manager
Handles all CSV file operations for requests, decisions, and audit logs
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import numpy as np
from config import (
    DATA_DIR, REQUESTS_CSV, DECISIONS_CSV, AUDIT_LOG_CSV,
    REQUEST_COLUMNS, DECISION_COLUMNS, AUDIT_LOG_COLUMNS
)


class DataManager:
    """Manages data persistence through CSV files"""
    
    def __init__(self):
        """Initialize data manager and ensure data directory exists"""
        self._ensure_data_dir()
        self._initialize_csv_files()
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
    
    def _initialize_csv_files(self):
        """Create CSV files with headers if they don't exist"""
        if not os.path.exists(REQUESTS_CSV):
            self._generate_sample_requests()
        
        if not os.path.exists(DECISIONS_CSV):
            self._generate_sample_decisions()
        
        if not os.path.exists(AUDIT_LOG_CSV):
            self._generate_sample_audit_log()
    
    def load_requests(self):
        """Load pending invoice requests from CSV"""
        try:
            df = pd.read_csv(REQUESTS_CSV, parse_dates=['original_due_date', 'submission_date'])
            return df
        except FileNotFoundError:
            # Return empty dataframe with correct columns
            return pd.DataFrame(columns=REQUEST_COLUMNS)
        except Exception as e:
            print(f"Error loading requests: {e}")
            return pd.DataFrame(columns=REQUEST_COLUMNS)
    
    def save_requests(self, df):
        """Save pending requests back to CSV"""
        try:
            df.to_csv(REQUESTS_CSV, index=False)
            return True
        except Exception as e:
            print(f"Error saving requests: {e}")
            return False
    
    def remove_request(self, request_id):
        """Remove a request from the pending list"""
        try:
            df = self.load_requests()
            df = df[df['request_id'] != request_id]
            self.save_requests(df)
            return True
        except Exception as e:
            print(f"Error removing request {request_id}: {e}")
            return False
    
    def load_decisions(self):
        """Load decision history from CSV"""
        try:
            df = pd.read_csv(DECISIONS_CSV, parse_dates=['decision_date'])
            return df
        except FileNotFoundError:
            return pd.DataFrame(columns=DECISION_COLUMNS)
        except Exception as e:
            print(f"Error loading decisions: {e}")
            return pd.DataFrame(columns=DECISION_COLUMNS)
    
    def add_decision(self, decision_data):
        """Append a new decision to the decisions CSV"""
        try:
            df = self.load_decisions()
            new_row = pd.DataFrame([decision_data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(DECISIONS_CSV, index=False)
            return True
        except Exception as e:
            print(f"Error adding decision: {e}")
            return False
    
    def load_audit_log(self):
        """Load audit log from CSV"""
        try:
            df = pd.read_csv(AUDIT_LOG_CSV, parse_dates=['timestamp'])
            return df
        except FileNotFoundError:
            return pd.DataFrame(columns=AUDIT_LOG_COLUMNS)
        except Exception as e:
            print(f"Error loading audit log: {e}")
            return pd.DataFrame(columns=AUDIT_LOG_COLUMNS)
    
    def add_audit_entry(self, action, user, request_id, details, ip_address="127.0.0.1"):
        """Add an entry to the audit log"""
        try:
            df = self.load_audit_log()
            new_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'action': action,
                'user': user,
                'request_id': request_id,
                'details': details,
                'ip_address': ip_address
            }
            new_row = pd.DataFrame([new_entry])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(AUDIT_LOG_CSV, index=False)
            return True
        except Exception as e:
            print(f"Error adding audit entry: {e}")
            return False
    
    def get_today_processed(self):
        """Get decisions processed today"""
        try:
            df = self.load_decisions()
            if df.empty:
                return df
            today = datetime.now().date()
            df['decision_date'] = pd.to_datetime(df['decision_date'])
            df_today = df[df['decision_date'].dt.date == today]
            return df_today
        except Exception as e:
            print(f"Error getting today's processed: {e}")
            return pd.DataFrame(columns=DECISION_COLUMNS)
    
    def get_statistics(self):
        """Calculate aggregate statistics"""
        try:
            requests_df = self.load_requests()
            decisions_df = self.load_decisions()
            today_df = self.get_today_processed()
            
            stats = {
                'pending_count': len(requests_df),
                'processed_today': len(today_df),
                'total_processed': len(decisions_df),
                'approved_count': len(decisions_df[decisions_df['final_decision'] == 'Approved']),
                'rejected_count': len(decisions_df[decisions_df['final_decision'] == 'Rejected']),
                'avg_amount': requests_df['invoice_amount'].mean() if not requests_df.empty else 0,
                'high_priority_count': len(requests_df[requests_df['priority'] == 'High']) if not requests_df.empty else 0,
                'total_pending_value': requests_df['invoice_amount'].sum() if not requests_df.empty else 0,
                'approval_rate': (len(decisions_df[decisions_df['final_decision'] == 'Approved']) / len(decisions_df) * 100) if len(decisions_df) > 0 else 0
            }
            return stats
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return {}
    
    def _generate_sample_requests(self):
        """Generate 30 sample pending requests"""
        np.random.seed(42)
        
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
        
        for i in range(1, 31):
            vendor = np.random.choice(vendors)
            amount = np.random.choice([
                np.random.uniform(3000, 15000),    # Low amounts
                np.random.uniform(15000, 35000),   # Medium amounts
                np.random.uniform(35000, 67000)    # High amounts
            ])
            
            due_date = base_date + timedelta(days=np.random.randint(2, 60))
            extension_days = np.random.choice([7, 14, 21, 30])
            priority = np.random.choice(['High', 'Medium', 'Low'], p=[0.25, 0.45, 0.30])
            vendor_reliability = np.random.uniform(0.70, 0.95)
            payment_history = np.random.uniform(0.75, 0.94)
            cash_flow = np.random.choice(['Low', 'Medium', 'High'], p=[0.30, 0.45, 0.25])
            submission_date = base_date - timedelta(days=np.random.randint(1, 10))
            
            requests.append({
                'request_id': f'REQ-{1000 + i}',
                'vendor_name': vendor,
                'invoice_amount': round(amount, 2),
                'original_due_date': due_date.strftime('%Y-%m-%d'),
                'requested_extension_days': extension_days,
                'reason': np.random.choice(reasons),
                'priority': priority,
                'vendor_reliability_score': round(vendor_reliability, 2),
                'payment_history_score': round(payment_history, 2),
                'cash_flow_impact': cash_flow,
                'submission_date': submission_date.strftime('%Y-%m-%d')
            })
        
        df = pd.DataFrame(requests)
        df.to_csv(REQUESTS_CSV, index=False)
        print(f"✅ Generated {len(requests)} sample requests")
    
    def _generate_sample_decisions(self):
        """Generate 50 sample historical decisions"""
        np.random.seed(43)
        
        vendors = [
            "Acme Corp", "TechGlobal Solutions", "MegaSoft Industries", 
            "DataFlow Systems", "CloudVentures Inc", "NextGen Technologies",
            "Prime Logistics", "Elite Manufacturing", "Global Trade Partners",
            "Innovative Solutions", "Strategic Services", "Precision Engineering"
        ]
        
        decisions = []
        base_date = datetime.now()
        
        # Generate distribution: 72% approved, 12% rejected, 16% escalated
        decision_types = ['Approved'] * 36 + ['Rejected'] * 6 + ['Approved'] * 8
        np.random.shuffle(decision_types)
        
        for i in range(1, 51):
            decision_date = base_date - timedelta(days=np.random.randint(1, 60), 
                                                  hours=np.random.randint(0, 23),
                                                  minutes=np.random.randint(0, 59))
            
            ai_decision = decision_types[i-1] if i <= len(decision_types) else 'Approved'
            final_decision = ai_decision
            
            # Higher confidence for approved, lower for rejected
            if ai_decision == 'Approved':
                confidence = np.random.uniform(0.70, 0.94)
            else:
                confidence = np.random.uniform(0.45, 0.75)
            
            amount = np.random.uniform(5000, 55000)
            processing_time = np.random.uniform(30, 300)
            
            decisions.append({
                'request_id': f'REQ-{900 + i}',
                'decision_date': decision_date.strftime('%Y-%m-%d %H:%M:%S'),
                'ai_decision': ai_decision,
                'confidence_score': round(confidence, 2),
                'human_review': np.random.choice([True, False], p=[0.15, 0.85]),
                'final_decision': final_decision,
                'processing_time_seconds': round(processing_time, 1),
                'vendor_name': np.random.choice(vendors),
                'invoice_amount': round(amount, 2)
            })
        
        df = pd.DataFrame(decisions)
        df.to_csv(DECISIONS_CSV, index=False)
        print(f"✅ Generated {len(decisions)} sample decisions")
    
    def _generate_sample_audit_log(self):
        """Generate sample audit log entries"""
        np.random.seed(44)
        
        actions = [
            "Decision: Approved", "Decision: Rejected", "Export: CSV", 
            "View: Dashboard", "View: Reports", "Login", "Data Refresh"
        ]
        
        users = ["Current User", "System Admin", "Finance Manager"]
        
        logs = []
        base_date = datetime.now()
        
        for i in range(25):
            timestamp = base_date - timedelta(days=np.random.randint(0, 30),
                                             hours=np.random.randint(0, 23),
                                             minutes=np.random.randint(0, 59))
            
            action = np.random.choice(actions)
            request_id = f'REQ-{np.random.randint(900, 1030)}' if 'Decision' in action else 'N/A'
            
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
                'user': np.random.choice(users),
                'request_id': request_id,
                'details': details,
                'ip_address': f'192.168.1.{np.random.randint(1, 255)}'
            })
        
        df = pd.DataFrame(logs)
        df = df.sort_values('timestamp', ascending=False)
        df.to_csv(AUDIT_LOG_CSV, index=False)
        print(f"✅ Generated {len(logs)} audit log entries")

