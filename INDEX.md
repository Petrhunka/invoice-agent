# Invoice Payment Manager - File Index

## 📂 Complete File Reference Guide

Quick reference for all files in the Invoice Payment Manager project.

---

## 🚀 START HERE

**For first-time users, read these in order:**

1. **README.md** - Complete documentation and overview
2. **QUICKSTART.md** - Step-by-step installation and first use
3. **verify_setup.py** - Run this to check your installation

---

## 📁 File Organization

### 🎯 Core Application Files (Required)

| File | Lines | Purpose |
|------|-------|---------|
| **main_simple.py** | 710 | Main Streamlit application with all 3 pages |
| **config.py** | 95 | Configuration, colors, thresholds, constants |
| **data_manager.py** | 268 | CSV operations and data management |
| **ai_decision_engine.py** | 242 | AI decision algorithm and risk scoring |
| **email_generator.py** | 188 | Email template generation |
| **styles.py** | 350 | Custom CSS and styled UI components |

### 💾 Data Files (Auto-Generated)

| File | Records | Purpose |
|------|---------|---------|
| **data/invoice_requests.csv** | 30 | Pending payment extension requests |
| **data/decisions.csv** | 50 | Historical decision records |
| **data/audit_log.csv** | 25 | Activity audit trail |

### 🔧 Setup & Configuration Files

| File | Purpose |
|------|---------|
| **requirements.txt** | Python package dependencies (5 packages) |
| **run.sh** | Application launch script with checks |
| **generate_sample_data.py** | Standalone script to regenerate CSV data |
| **verify_setup.py** | Installation verification script |
| **.streamlit/config.toml** | Streamlit theme configuration (light mode) |

### 📚 Documentation Files

| File | Size | Purpose |
|------|------|---------|
| **README.md** | 500+ lines | Complete user and technical documentation |
| **QUICKSTART.md** | 400+ lines | Getting started guide with tutorials |
| **TESTING_CHECKLIST.md** | 600+ lines | Comprehensive testing and verification guide |
| **PROJECT_SUMMARY.md** | 450+ lines | Project overview and deliverables summary |
| **INDEX.md** | This file | File reference and navigation guide |
| **LOGO_PLACEHOLDER.txt** | Short | Instructions for adding Keboola logo |

---

## 📖 Documentation Guide

### When to Read What

**Just Starting?**
→ README.md (overview) → QUICKSTART.md (hands-on) → run the app!

**Installing for First Time?**
→ QUICKSTART.md (sections 1-4) → verify_setup.py → run.sh

**Want to Test Everything?**
→ TESTING_CHECKLIST.md (complete verification)

**Need Technical Details?**
→ README.md (full reference) → PROJECT_SUMMARY.md (architecture)

**Customizing the App?**
→ config.py (settings) → README.md (configuration section)

**Troubleshooting?**
→ README.md (troubleshooting) → QUICKSTART.md (common operations)

**For Project Handoff?**
→ PROJECT_SUMMARY.md (deliverables overview)

---

## 🎯 Quick File Lookup

### "I want to..."

**...launch the application**
→ `run.sh` or `streamlit run main_simple.py`

**...check if everything is installed correctly**
→ Run `python3 verify_setup.py`

**...understand how the AI works**
→ Read `ai_decision_engine.py` or README.md AI section

**...change the color scheme**
→ Edit `config.py` → KEBOOLA_COLORS

**...modify decision thresholds**
→ Edit `config.py` → DECISION_RULES

**...customize email templates**
→ Edit `email_generator.py`

**...add new charts or UI elements**
→ Edit `main_simple.py` and `styles.py`

**...regenerate sample data**
→ Run `python3 generate_sample_data.py`

**...add my own data**
→ Edit CSV files in `data/` directory

**...add the Keboola logo**
→ Read `LOGO_PLACEHOLDER.txt` for instructions

---

## 🔍 File Details

### main_simple.py (Entry Point)
**What it does**: Complete Streamlit application
**Contains**:
- Session state initialization
- Sidebar navigation
- Dashboard page with metrics and charts
- Review Requests page with AI decision workflow
- Reports page with 4 tabs
- All UI rendering functions

**Key Functions**:
- `main()` - Application entry point
- `render_dashboard()` - Page 1
- `render_review_requests()` - Page 2
- `render_reports()` - Page 3
- `process_decision()` - Save decisions

**To modify**: Edit page layouts, add features, change UI

---

### config.py (Configuration)
**What it does**: Central configuration file
**Contains**:
- Color palette (9 colors)
- Decision rules and thresholds
- Risk assessment boundaries
- Feature weights (6 factors)
- CSV paths and column definitions

**Key Constants**:
- `KEBOOLA_COLORS` - Brand colors
- `DECISION_RULES` - AI thresholds
- `FEATURE_WEIGHTS` - Risk calculation weights
- `RISK_THRESHOLDS` - Color coding boundaries

**To modify**: Change any setting without touching main code

---

### data_manager.py (Data Layer)
**What it does**: All CSV file operations
**Contains**:
- DataManager class with 8 methods
- Sample data generation (3 functions)
- Statistics calculation

**Key Methods**:
- `load_requests()` - Read pending requests
- `save_requests()` - Write pending requests
- `add_decision()` - Append decision record
- `add_audit_entry()` - Log activities
- `get_statistics()` - Calculate metrics

**To modify**: Change data operations, add new CSV files

---

### ai_decision_engine.py (AI Logic)
**What it does**: AI decision algorithm
**Contains**:
- AIDecisionEngine class
- Risk score calculation (6 weighted factors)
- Confidence score calculation
- Decision logic (Approve/Reject/Escalate)

**Key Methods**:
- `make_decision()` - Main decision function
- `_calculate_risk_score()` - Weighted risk
- `_calculate_confidence_score()` - Confidence
- `_determine_decision()` - Final decision
- `_generate_reasoning()` - Human explanation

**To modify**: Adjust algorithm, add factors, change logic

---

### email_generator.py (Email Templates)
**What it does**: Generate formatted emails
**Contains**:
- 4 template functions
- Dynamic field population
- Professional formatting

**Key Functions**:
- `format_original_email()` - Vendor request
- `generate_approval_email()` - Approval response
- `generate_rejection_email()` - Rejection response
- `generate_email_response()` - Wrapper function

**To modify**: Edit email templates, add new fields

---

### styles.py (Custom Styling)
**What it does**: CSS and styled components
**Contains**:
- 300+ lines of custom CSS
- 6 styled UI component functions
- Keboola branding elements

**Key Functions**:
- `load_custom_css()` - Inject CSS
- `render_metric_card()` - Styled metrics
- `render_factor_indicator()` - Color-coded factors
- `render_header_with_logo()` - Branded header
- `render_email_preview()` - Email display

**To modify**: Change styling, add new components

---

### requirements.txt (Dependencies)
**What it does**: Lists required Python packages
**Contains**:
```
streamlit==1.29.0
pandas==2.1.4
plotly==5.18.0
numpy==1.26.2
python-dateutil==2.8.2
```

**To install**: `pip3 install -r requirements.txt`

---

### run.sh (Launch Script)
**What it does**: Easy application startup
**Contains**:
- Python version check
- Dependency verification
- Auto-installation option
- Streamlit launch command

**To run**: `./run.sh` or `bash run.sh`

---

### generate_sample_data.py (Data Generator)
**What it does**: Creates sample CSV files
**Contains**:
- 3 generation functions
- 30 requests, 50 decisions, 25 audit logs
- Realistic random data

**When to run**:
- First installation
- After deleting CSV files
- Want fresh sample data

**To run**: `python3 generate_sample_data.py`

---

### verify_setup.py (Verification Tool)
**What it does**: Checks installation completeness
**Contains**:
- 6 verification checks
- Python version check
- File existence verification
- Dependency check
- Data validation

**When to run**:
- After installation
- Before first use
- After troubleshooting

**To run**: `python3 verify_setup.py`

---

## 📊 Data File Formats

### invoice_requests.csv (11 columns)
```
request_id, vendor_name, invoice_amount, original_due_date,
requested_extension_days, reason, priority, vendor_reliability_score,
payment_history_score, cash_flow_impact, submission_date
```

### decisions.csv (9 columns)
```
request_id, decision_date, ai_decision, confidence_score,
human_review, final_decision, processing_time_seconds,
vendor_name, invoice_amount
```

### audit_log.csv (6 columns)
```
timestamp, action, user, request_id, details, ip_address
```

---

## 🛠️ Modification Guide

### To Change Colors
1. Open `config.py`
2. Edit `KEBOOLA_COLORS` dictionary
3. Save and rerun app

### To Adjust AI Thresholds
1. Open `config.py`
2. Edit `DECISION_RULES` or `RISK_THRESHOLDS`
3. Save and rerun app

### To Add New Feature
1. Edit `main_simple.py`
2. Add function for new feature
3. Call from appropriate page function
4. Update `styles.py` if styling needed

### To Modify Email Templates
1. Open `email_generator.py`
2. Edit template functions
3. Test with sample decision

### To Add New Report Tab
1. Edit `render_reports()` in `main_simple.py`
2. Add new tab in `st.tabs()`
3. Create rendering logic

---

## 📦 Complete File Listing

```
invoice-agent/
├── Core Application (6 files, ~2,500 lines)
│   ├── main_simple.py              710 lines
│   ├── config.py                    95 lines
│   ├── data_manager.py             268 lines
│   ├── ai_decision_engine.py       242 lines
│   ├── email_generator.py          188 lines
│   └── styles.py                   350 lines
│
├── Data Files (3 files, 105 records)
│   ├── data/
│   │   ├── invoice_requests.csv     30 records
│   │   ├── decisions.csv            50 records
│   │   └── audit_log.csv            25 records
│
├── Configuration Files (2 files)
│   ├── .streamlit/
│   │   └── config.toml              Theme configuration
│   └── requirements.txt              5 dependencies
│
├── Setup Files (3 files)
│   ├── run.sh                       30 lines
│   ├── generate_sample_data.py     150 lines
│   └── verify_setup.py             200 lines
│
├── Documentation (6 files, ~2,500 lines)
│   ├── README.md                   500+ lines
│   ├── QUICKSTART.md               400+ lines
│   ├── TESTING_CHECKLIST.md        600+ lines
│   ├── PROJECT_SUMMARY.md          450+ lines
│   ├── INDEX.md                    (this file)
│   └── LOGO_PLACEHOLDER.txt         short
│
└── Auto-Generated
    └── __pycache__/                (Python bytecode)
```

**Total**: 19 files (excluding pycache)
**Total Code**: ~5,300 lines

---

## 🎓 Learning Path

### For End Users
1. README.md - Overview
2. QUICKSTART.md - Tutorial
3. Run the app - Hands-on
4. TESTING_CHECKLIST.md - Verification

### For Administrators
1. README.md - Full documentation
2. verify_setup.py - Installation check
3. config.py - Configuration options
4. PROJECT_SUMMARY.md - Architecture

### For Developers
1. PROJECT_SUMMARY.md - Overview
2. Code files - Implementation
3. config.py - Settings
4. README.md - API reference

### For Testers
1. TESTING_CHECKLIST.md - Complete test suite
2. generate_sample_data.py - Fresh test data
3. verify_setup.py - Environment check

---

## 🔄 File Dependencies

```
main_simple.py
├── imports config.py
├── imports data_manager.py
├── imports ai_decision_engine.py
├── imports email_generator.py
└── imports styles.py

data_manager.py
└── imports config.py

ai_decision_engine.py
└── imports config.py

email_generator.py
└── (no local dependencies)

styles.py
└── imports config.py

generate_sample_data.py
└── (standalone, no dependencies)

verify_setup.py
└── (standalone, no dependencies)
```

---

## ✅ Quick Checklist

Use this to verify you have everything:

**Core Files**
- [ ] main_simple.py
- [ ] config.py
- [ ] data_manager.py
- [ ] ai_decision_engine.py
- [ ] email_generator.py
- [ ] styles.py

**Data Files**
- [ ] data/invoice_requests.csv
- [ ] data/decisions.csv
- [ ] data/audit_log.csv

**Setup Files**
- [ ] requirements.txt
- [ ] run.sh (executable)
- [ ] generate_sample_data.py
- [ ] verify_setup.py (executable)

**Documentation**
- [ ] README.md
- [ ] QUICKSTART.md
- [ ] TESTING_CHECKLIST.md
- [ ] PROJECT_SUMMARY.md
- [ ] INDEX.md
- [ ] LOGO_PLACEHOLDER.txt

---

## 🎯 Next Steps

1. **If not yet installed**: Follow QUICKSTART.md
2. **If installed**: Run `./verify_setup.py`
3. **If verified**: Run `./run.sh`
4. **If running**: Open http://localhost:8501
5. **If using**: Refer to README.md as needed

---

## 📞 Getting Help

**Issue**: Can't find a file
→ Check this INDEX.md

**Issue**: Don't know where to start
→ Read QUICKSTART.md

**Issue**: Installation problems
→ Run verify_setup.py

**Issue**: How to use the app
→ Read README.md

**Issue**: Want to customize
→ Check config.py first

**Issue**: Need technical details
→ Read PROJECT_SUMMARY.md

**Issue**: Testing the app
→ Use TESTING_CHECKLIST.md

---

**Made with ❤️ by Keboola**

*For the latest updates, check PROJECT_SUMMARY.md*

