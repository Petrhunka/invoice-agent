# Invoice Payment Manager - AI Agent

<div align="center">

**Streamlit-based Invoice Payment Extension Request Management System**

*Powered by Keboola*

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.29.0-FF4B4B.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## 📋 Overview

The Invoice Payment Manager is an intelligent application designed to help Shared Service Centers (SSCs) efficiently process vendor payment extension requests. It combines AI-driven decision support with transparent explanations and automated email generation.

### Key Features

- 🤖 **AI-Powered Decisions**: Weighted scoring algorithm with 6-factor risk assessment
- 📊 **Live Dashboard**: Real-time metrics, charts, and request tracking
- 📋 **Review Workflow**: Streamlined approve/reject process with email generation
- 💼 **Dual Explanations**: Business-friendly and technical AI explanations
- 📈 **Comprehensive Reports**: Analytics, history, and audit trails
- 💾 **CSV Persistence**: Simple file-based data storage
- 🎨 **Keboola Branding**: Professional blue color scheme

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the repository**
```bash
cd invoice-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
# Option 1: Using the launch script
./run.sh

# Option 2: Direct Streamlit command
streamlit run main_simple.py
```

4. **Access the application**
Open your browser to: `http://localhost:8501`

---

## 📁 Project Structure

```
invoice-agent/
├── main_simple.py              # Main Streamlit application (3 pages)
├── config.py                   # Configuration, colors, thresholds
├── styles.py                   # Custom CSS and UI components
├── data_manager.py             # CSV data operations
├── ai_decision_engine.py       # AI decision logic
├── email_generator.py          # Email template generation
├── logo_blue.png               # Keboola logo (optional)
├── .streamlit/
│   └── config.toml             # Streamlit theme config (light mode)
├── data/
│   ├── invoice_requests.csv    # Pending requests (30 samples)
│   ├── decisions.csv           # Decision history (50 samples)
│   └── audit_log.csv           # Activity log
├── requirements.txt            # Python dependencies
├── run.sh                      # Launch script
└── README.md                   # This file
```

---

## 🎯 Application Pages

### 1. 🏠 Dashboard

**Features:**
- Session info bar (duration, processed count, approval rate)
- 4 metric cards: Pending, Processed Today, Avg Amount, High Priority
- 2 interactive charts: Amount Distribution, Priority Breakdown
- Recent requests and decisions tables

**Purpose:** Get a quick overview of all pending and processed requests.

---

### 2. 📋 Review Requests

**Features:**
- Request selector dropdown
- Two-column layout:
  - **Left**: Original vendor email
  - **Right**: AI recommendation with scores
- AI explanation toggle:
  - **Business**: Color-coded factors (🟢🟡🔴) with plain language
  - **Technical**: Formulas, calculations, performance metrics
- Approve/Reject buttons
- Email preview before sending
- One-click send & complete

**Purpose:** Review requests with full AI transparency and make informed decisions.

---

### 3. 📊 Reports

**Four Tabs:**

**Tab 1: All Pending Requests**
- Full table with filters (priority, amount, vendor)
- CSV export

**Tab 2: Decision History**
- Historical decisions with filters
- Date range, decision type, confidence score
- CSV export

**Tab 3: Analytics**
- Line chart: Decisions over time
- Box plot: Amount by decision type
- Histogram: Confidence distribution
- Summary statistics

**Tab 4: Audit Log**
- Complete activity log
- Filter by action and user
- CSV export

**Purpose:** Access comprehensive reports and analytics for all activities.

---

## 🤖 AI Decision Engine

### Algorithm: Rule-Based Weighted Scoring

**6 Key Factors:**

| Factor | Weight | Description |
|--------|--------|-------------|
| Invoice Amount | 25% | Higher amounts = higher risk |
| Extension Period | 20% | Longer extensions = higher risk |
| Vendor Reliability | 20% | Historical reliability score |
| Payment History | 15% | Past payment performance |
| Cash Flow Impact | 15% | Impact on company cash flow |
| Priority Level | 5% | Request urgency |

### Risk Score Calculation

```
Risk = (Amount × 0.25) + (Extension × 0.20) + (Vendor × 0.20) 
     + (Payment × 0.15) + (CashFlow × 0.15) + (Priority × 0.05)
```

### Confidence Score

```
Base = (Vendor_Reliability + Payment_History) / 2
Amount_Factor = 1.0 - min(Amount / 100000, 0.3)
Confidence = Base × Amount_Factor
```

### Decision Logic

- **Approved**: High confidence (≥80%) + Low risk (<40%)
- **Rejected**: Low confidence (<60%) or High risk (>70%) with amount ≤$50k
- **Escalate**: Uncertain cases or high-value transactions (>$50k)

---

## 🎨 Color-Coded Factor System

### Risk Thresholds

**Invoice Amount:**
- 🟢 **GREEN**: < $20,000 (Low Risk)
- 🟡 **YELLOW**: $20,000 - $50,000 (Medium)
- 🔴 **RED**: > $50,000 (High Risk)

**Extension Days:**
- 🟢 **GREEN**: ≤ 14 days (Short)
- 🟡 **YELLOW**: 15-21 days (Moderate)
- 🔴 **RED**: > 21 days (Long Period)

**Vendor Reliability:**
- 🟢 **GREEN**: > 85% (Excellent)
- 🟡 **YELLOW**: 70-85% (Good)
- 🔴 **RED**: < 70% (Concerning)

**Payment History:**
- 🟢 **GREEN**: > 85% (Excellent)
- 🟡 **YELLOW**: 70-85% (Good)
- 🔴 **RED**: < 70% (Needs Review)

**Cash Flow Impact:**
- 🟢 **GREEN**: Low (Low Impact)
- 🟡 **YELLOW**: Medium (Medium Impact)
- 🔴 **RED**: High (High Impact)

**Priority:**
- 🟢 **GREEN**: Low
- 🟡 **YELLOW**: Medium
- 🔴 **RED**: High

---

## 📧 Email Templates

### Approval Email
- Subject line with request ID
- Request details section
- Approval details with confidence score
- New due date calculation
- Important reminders
- Professional closing

### Rejection Email
- Subject line with request ID
- Request details
- Decision reasoning
- Next steps
- Alternative options
- Contact information

Both templates are automatically generated and can be previewed before sending.

---

## 💾 Data Management

### CSV Files

**invoice_requests.csv** (Pending Queue)
- 11 columns including request_id, vendor_name, amount, dates, scores
- Auto-generated with 30 realistic samples
- Updated when requests are processed

**decisions.csv** (History)
- 9 columns including decision details, confidence, processing time
- Starts with 50 historical records
- Grows as decisions are made

**audit_log.csv** (Activity Log)
- 6 columns tracking all user actions
- Timestamps, actions, users, details
- Comprehensive audit trail

### Session State Management

- Data loaded **once** at application start
- In-memory updates during session
- CSV writes on every decision
- Manual refresh button available
- No constant file reloading

---

## 🔧 Configuration

### Theme Settings (.streamlit/config.toml)

The application uses **light theme** by default for optimal readability:

```toml
[theme]
primaryColor = "#1F8FFF"              # Keboola blue
backgroundColor = "#FFFFFF"            # White background
secondaryBackgroundColor = "#F5F5F5"  # Light gray
textColor = "#212121"                 # Dark text
base = "light"                        # Force light theme
```

All UI elements are optimized for light theme with proper contrast ratios.

### Application Settings (config.py)

Edit `config.py` to customize:

```python
# Color scheme
KEBOOLA_COLORS = {
    "primary_blue": "#1F8FFF",
    "dark_blue": "#0D47A1",
    # ... more colors
}

# Decision rules
DECISION_RULES = {
    "auto_approve_threshold": 0.8,
    "high_risk_amount": 50000,
    # ... more thresholds
}

# Risk thresholds
RISK_THRESHOLDS = {
    "amount": {"low": 20000, "high": 50000},
    # ... more thresholds
}
```

---

## 🎯 User Workflow

1. **Open Dashboard** → View pending requests and metrics
2. **Navigate to Review** → Select a request to review
3. **Read Original Email** → Understand vendor's situation
4. **Review AI Analysis** → Check recommendation and factors
5. **Expand Explanation** → Choose Business or Technical view
6. **Make Decision** → Click Approve or Reject
7. **Preview Email** → Review generated response
8. **Send & Complete** → Finalize decision (saves to CSV, updates audit log)
9. **Return to Dashboard** → See updated metrics

---

## 📊 Sample Data

### Included Samples

- **30 Pending Requests**
  - 15 unique vendors
  - Amounts: $3,000 - $67,000
  - Various priorities and extension periods
  - Realistic vendor and payment scores

- **50 Historical Decisions**
  - 60-day date range
  - 72% approved, 12% rejected, 16% escalated
  - Confidence scores: 0.45 - 0.94
  - Processing times: 30-300 seconds

- **25 Audit Log Entries**
  - Various action types
  - Multiple users
  - Recent timestamps

---

## 🛠️ Troubleshooting

### Application won't start
```bash
# Check Python version
python3 --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Clear Streamlit cache
rm -rf ~/.streamlit/
```

### Data not loading
```bash
# Check if data directory exists
ls -la data/

# Regenerate sample data (delete CSVs first)
rm data/*.csv
streamlit run main_simple.py
```

### Port already in use
```bash
# Use different port
streamlit run main_simple.py --server.port 8502
```

---

## 🚀 Advanced Usage

### Custom Logo

1. Place `logo_blue.png` in the project root
2. Uncomment logo lines in `main_simple.py`:
```python
# Line 46 (sidebar)
st.image("logo_blue.png", width=150)

# Lines 98-100 (header)
with open("logo_blue.png", "rb") as f:
    logo_data = base64.b64encode(f.read()).decode()
st.markdown(render_header_with_logo(logo_data), unsafe_allow_html=True)
```

### Adding Your Own Data

Replace the sample CSV files in `data/` directory with your own data matching the column structure.

### Customizing Decision Rules

Edit thresholds in `config.py`:
```python
DECISION_RULES = {
    "auto_approve_threshold": 0.85,  # Stricter
    "high_risk_amount": 40000,        # Lower threshold
}
```

---

## 📝 Dependencies

```
streamlit==1.29.0     # Web application framework
pandas==2.1.4         # Data manipulation
plotly==5.18.0        # Interactive charts
numpy==1.26.2         # Numerical operations
python-dateutil==2.8.2  # Date parsing
```

---

## 🤝 Contributing

This is an internal Keboola tool. For feature requests or bug reports, contact the development team.

---

## 📄 License

Copyright © 2025 Keboola. All rights reserved.

---

## 👥 Support

For questions or issues:
- **Email**: support@keboola.com
- **Internal**: Slack #invoice-ai-agent

---

## 🎉 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io) - Web framework
- [Plotly](https://plotly.com) - Interactive visualizations
- [Pandas](https://pandas.pydata.org) - Data processing

**Made with ❤️ by Keboola**

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Plotly Python Documentation](https://plotly.com/python/)
- [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

---

**Version**: 1.0.0  
**Last Updated**: October 24, 2025  
**Status**: Production Ready ✅

