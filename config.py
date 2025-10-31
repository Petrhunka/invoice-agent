"""
Configuration file for Invoice Payment Manager
Contains color schemes, thresholds, and application constants
"""

# Keboola Brand Colors
KEBOOLA_COLORS = {
    "primary_blue": "#1F8FFF",      # Main brand color
    "dark_blue": "#0D47A1",         # Darker accents
    "light_blue": "#E3F2FD",        # Backgrounds
    "success_green": "#4CAF50",     # Approvals
    "warning_yellow": "#FFC107",    # Warnings
    "danger_red": "#F44336",        # Rejections
    "neutral_gray": "#F5F5F5",      # Sidebar
    "text_dark": "#212121",         # Primary text
    "text_light": "#757575"         # Secondary text
}

# Application Settings
APP_TITLE = "AI Invoice Auditor"
APP_SUBTITLE = "Powered by Keboola"
COMPANY_NAME = "Keboola"

# AI Decision Rules
DECISION_RULES = {
    "auto_approve_threshold": 0.8,
    "auto_reject_threshold": 0.3,
    "max_extension_days": 30,
    "min_confidence_score": 0.6,
    "high_risk_amount": 50000,
    "escalate_confidence_threshold": 0.6,
    "escalate_risk_threshold": 0.7,
    "low_risk_threshold": 0.4,
}

# Risk Assessment Thresholds
RISK_THRESHOLDS = {
    "amount": {
        "low": 20000,
        "high": 50000
    },
    "extension_days": {
        "low": 14,
        "high": 21
    },
    "vendor_reliability": {
        "excellent": 0.85,
        "good": 0.70
    },
    "payment_history": {
        "excellent": 0.85,
        "good": 0.70
    }
}

# Feature Weights for Risk Calculation
FEATURE_WEIGHTS = {
    "amount": 0.25,
    "extension": 0.20,
    "vendor": 0.20,
    "payment": 0.15,
    "cash_flow": 0.15,
    "priority": 0.05
}

# Cash Flow Impact Mapping
CASH_FLOW_RISK = {
    "Low": 0.2,
    "Medium": 0.5,
    "High": 0.8
}

# Priority Risk Mapping
PRIORITY_RISK = {
    "Low": 0.3,
    "Medium": 0.5,
    "High": 0.7
}

# Data Paths
DATA_DIR = "data"
REQUESTS_CSV = f"{DATA_DIR}/invoice_requests.csv"
DECISIONS_CSV = f"{DATA_DIR}/decisions.csv"
AUDIT_LOG_CSV = f"{DATA_DIR}/audit_log.csv"

# CSV Column Definitions
REQUEST_COLUMNS = [
    "request_id", "vendor_name", "invoice_amount", "original_due_date",
    "requested_extension_days", "reason", "priority", "vendor_reliability_score",
    "payment_history_score", "cash_flow_impact", "submission_date"
]

DECISION_COLUMNS = [
    "request_id", "decision_date", "ai_decision", "confidence_score",
    "human_review", "final_decision", "processing_time_seconds",
    "vendor_name", "invoice_amount"
]

AUDIT_LOG_COLUMNS = [
    "timestamp", "action", "user", "request_id", "details", "ip_address"
]

