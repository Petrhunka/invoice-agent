# Testing Checklist - Invoice Payment Manager

## 🧪 Complete Feature Verification

Use this checklist to verify all features are working correctly after installation or updates.

---

## ✅ Installation & Setup

- [ ] Python 3.8+ installed and verified
- [ ] All dependencies installed (`pip3 install -r requirements.txt`)
- [ ] Data directory exists with 3 CSV files
- [ ] Sample data generated (30 requests, 50 decisions, 25 audit logs)
- [ ] run.sh has executable permissions
- [ ] Application launches without errors
- [ ] Browser opens to localhost:8501

---

## ✅ Page 1: Dashboard

### Header & Branding
- [ ] Header displays "Invoice AI Agent"
- [ ] Subtitle shows "Powered by Keboola"
- [ ] Blue gradient background on header
- [ ] Logo placeholder comment present (if logo not available)

### Session Info Bar
- [ ] Session duration timer displays (HH:MM:SS format)
- [ ] Processed count shows correct number
- [ ] Approval rate calculates correctly
- [ ] Light blue background with proper styling

### Metric Cards (4 columns)
- [ ] **Pending Requests**: Shows correct count
- [ ] **Processed Today**: Shows daily total
- [ ] **Avg Request Amount**: Displays formatted currency
- [ ] **High Priority**: Shows high-priority count
- [ ] All cards have blue left border
- [ ] Gradient backgrounds display correctly
- [ ] Delta values show appropriate context

### Charts (2 columns)
- [ ] **Amount Distribution**: Histogram renders
- [ ] Chart uses Keboola blue color
- [ ] 15 bins distributed correctly
- [ ] **Priority Breakdown**: Pie chart renders
- [ ] Colors match: High=Red, Medium=Yellow, Low=Green
- [ ] Percentages display correctly
- [ ] Charts are interactive (hover shows values)

### Tables (2 columns)
- [ ] **Pending Requests**: Shows top 10
- [ ] Columns: request_id, vendor_name, invoice_amount, priority, original_due_date
- [ ] Amounts formatted as currency
- [ ] **Recently Processed**: Shows top 10 decisions
- [ ] Sorted by decision_date descending
- [ ] Both tables have white backgrounds
- [ ] Text is dark and readable
- [ ] Alternating row colors work

### Navigation
- [ ] Sidebar navigation works
- [ ] Can switch to other pages
- [ ] Returns to dashboard correctly

---

## ✅ Page 2: Review Requests

### Request Selection
- [ ] Dropdown lists all pending requests
- [ ] Format: "REQ-XXXX - Vendor Name ($XX,XXX.XX)"
- [ ] Can select different requests
- [ ] Selection triggers content update

### Left Column: Original Email
- [ ] Text area displays formatted vendor email
- [ ] Height is 400px
- [ ] Contains all email headers (From, To, Date, Subject)
- [ ] Shows vendor name, amount, due date, extension days
- [ ] Includes reason for extension
- [ ] Proper separator lines (━━━)
- [ ] Readable font and spacing

### Right Column: AI Recommendation
- [ ] Decision displays with color:
  - [ ] ✅ APPROVED in green
  - [ ] ❌ REJECTED in red
  - [ ] ⚡ ESCALATE in yellow
- [ ] Confidence score shows percentage
- [ ] Confidence progress bar renders
- [ ] Risk score shows percentage
- [ ] Risk progress bar renders
- [ ] Brief reasoning displays
- [ ] Request details list shows 6 items:
  - [ ] Request ID
  - [ ] Vendor
  - [ ] Amount (formatted)
  - [ ] Extension days
  - [ ] Priority
  - [ ] Due date

### AI Explanation Section
- [ ] Radio buttons for explanation type present
- [ ] "💼 Business Explanation" option works
- [ ] "🔬 Technical Explanation" option works
- [ ] Expander widget displays
- [ ] Opens/closes correctly

### Business Explanation
- [ ] Title: "💼 Business Explanation"
- [ ] Subtitle: "Understanding the decision factors..."
- [ ] 6 factor cards render:
  1. [ ] **Invoice Amount**: Shows value, weight (25%), status
  2. [ ] **Extension Period**: Shows days, weight (20%), status
  3. [ ] **Vendor Reliability**: Shows %, weight (20%), status
  4. [ ] **Payment History**: Shows %, weight (15%), status
  5. [ ] **Cash Flow Impact**: Shows level, weight (15%), status
  6. [ ] **Priority Level**: Shows level, weight (5%), status
- [ ] Color indicators work correctly:
  - [ ] 🟢 Green for favorable/low risk
  - [ ] 🟡 Yellow for moderate
  - [ ] 🔴 Red for concerning/high risk
- [ ] Factor Impact Summary table displays
- [ ] Shows Factor, Weight, Risk Contribution columns
- [ ] Overall Assessment section shows:
  - [ ] Total Risk Score with interpretation
  - [ ] Confidence Level with interpretation
  - [ ] Correct color coding (green/yellow/red boxes)
- [ ] Final AI Recommendation displays with reasoning

### Technical Explanation
- [ ] Title: "🔬 Technical Explanation"
- [ ] Model Architecture expander works
- [ ] Feature Engineering table displays:
  - [ ] 6 rows (one per feature)
  - [ ] Columns: Feature, Raw Value, Normalized, Formula
  - [ ] Values match request data
- [ ] Risk Score Calculation shows:
  - [ ] LaTeX formula renders correctly
  - [ ] Weighted formula displays
  - [ ] Actual calculation breakdown
  - [ ] Total Risk Score metric
- [ ] Confidence Score Calculation shows:
  - [ ] LaTeX formulas render
  - [ ] Base confidence calculation
  - [ ] Amount factor calculation
  - [ ] Final confidence with actual values
- [ ] Decision Tree Logic:
  - [ ] Python code block displays
  - [ ] Code is properly formatted
  - [ ] Shows complete decision logic
- [ ] Model Performance Metrics:
  - [ ] 4 metrics display (Precision, Recall, F1, AUC-ROC)
  - [ ] Values are reasonable (0.89, 0.92, 0.90, 0.94)
- [ ] Feature Importance Chart:
  - [ ] Horizontal bar chart renders
  - [ ] 6 bars (one per feature)
  - [ ] Weights match (25%, 20%, 20%, 15%, 15%, 5%)
  - [ ] Blue color gradient

### Decision Buttons
- [ ] Two buttons visible: ✅ APPROVE and ❌ REJECT
- [ ] APPROVE button is primary style (blue)
- [ ] REJECT button is secondary style
- [ ] Buttons are responsive
- [ ] Clicking stores decision in session state

### Email Preview (After Decision)
- [ ] Section appears after clicking approve/reject
- [ ] Title: "📨 Email Preview"
- [ ] Two columns layout:
  - [ ] Left: Original Request (repeated)
  - [ ] Right: Response Email
- [ ] Response email appropriate for decision:
  - [ ] **Approval**: Contains new due date, approval details
  - [ ] **Rejection**: Contains reasoning, next steps
- [ ] Both emails properly formatted with separators
- [ ] "📤 Send Email & Complete" button appears (primary)
- [ ] "❌ Cancel" button appears
- [ ] Cancel clears pending decision and reloads page

### Decision Processing
- [ ] Click "Send Email & Complete"
- [ ] Success message displays
- [ ] Balloons animation plays 🎉
- [ ] Decision saved to decisions.csv
- [ ] Request removed from invoice_requests.csv
- [ ] Audit log entry created
- [ ] Session state counters update
- [ ] Page reloads with fresh data
- [ ] Dashboard metrics reflect change
- [ ] Processed count increments

---

## ✅ Page 3: Reports

### Top Metrics
- [ ] 4 metric cards in row:
  - [ ] Total Pending
  - [ ] Total Processed
  - [ ] Approved
  - [ ] Rejected
- [ ] All counts accurate

### Tab 1: All Pending Requests
- [ ] Tab labeled "📋 All Pending Requests"
- [ ] Filter section displays with 3 columns:
  - [ ] Priority multiselect (High, Medium, Low)
  - [ ] Amount range slider (0 to max)
  - [ ] Vendor multiselect (all vendors listed)
- [ ] Default: All options selected
- [ ] Table shows all 11 columns
- [ ] Filters update table immediately
- [ ] "📥 Download CSV" button present
- [ ] Download works and saves with today's date
- [ ] CSV contains filtered data
- [ ] Empty state message if no requests

### Tab 2: Decision History
- [ ] Tab labeled "📜 Decision History"
- [ ] Filter section displays with 3 columns:
  - [ ] Decision type multiselect (Approved, Rejected)
  - [ ] Date range slider (days back: 1-90)
  - [ ] Min confidence slider (0.0-1.0)
- [ ] Table shows all 9 decision columns
- [ ] Filters work correctly
- [ ] Download CSV button present and functional
- [ ] Empty state message if no decisions

### Tab 3: Analytics
- [ ] Tab labeled "📈 Analytics"
- [ ] **Decisions Over Time**:
  - [ ] Line chart renders
  - [ ] X-axis: Date
  - [ ] Y-axis: Count
  - [ ] Separate lines for Approved (green) and Rejected (red)
  - [ ] Legend displays
  - [ ] Interactive hover tooltips
- [ ] Two charts in columns:
  - [ ] **Amount Distribution by Decision**:
    - [ ] Box plot renders
    - [ ] X-axis: Decision type
    - [ ] Y-axis: Invoice amount
    - [ ] Color-coded boxes (green/red)
  - [ ] **Confidence Score Distribution**:
    - [ ] Histogram renders
    - [ ] 20 bins
    - [ ] Color by decision type
    - [ ] Overlapping or stacked bars
- [ ] **Summary Statistics** (4 metrics):
  - [ ] Avg Confidence (percentage)
  - [ ] Avg Processing Time (seconds)
  - [ ] Total Value Processed (currency)
  - [ ] Approval Rate (percentage)
- [ ] All calculations correct
- [ ] Empty state message if no data

### Tab 4: Audit Log
- [ ] Tab labeled "🔍 Audit Log"
- [ ] Filter section with 2 columns:
  - [ ] Action type multiselect (all actions)
  - [ ] User multiselect (all users)
- [ ] Table shows all 6 audit columns
- [ ] Sorted by timestamp descending
- [ ] Filters work correctly
- [ ] Download CSV button functional
- [ ] Empty state message if no logs

---

## ✅ Sidebar Functionality

### Logo
- [ ] Placeholder comment present (or logo displays if available)
- [ ] 150px width specification

### Title & Branding
- [ ] "🏢 Invoice Payment Manager" displays
- [ ] "*by Keboola*" subtitle in italics
- [ ] Separator line below

### Navigation Radio Buttons
- [ ] Three options:
  - [ ] 🏠 Dashboard
  - [ ] 📋 Review Requests
  - [ ] 📊 Reports
- [ ] Selection changes active page
- [ ] Active page highlights
- [ ] Navigation smooth (no flickering)

### Quick Stats
- [ ] Section title: "📊 Quick Stats"
- [ ] Pending metric displays
- [ ] Processed metric with approval % displays
- [ ] Updates in real-time after decisions
- [ ] Separator line below

### Data Status
- [ ] Section title: "💾 Data Status"
- [ ] "✓ Data loaded" success message
- [ ] "🔄 Refresh from CSV" button present
- [ ] Button triggers data reload
- [ ] Success message appears after refresh
- [ ] All pages update with fresh data

---

## ✅ Styling & Design

### Colors
- [ ] Primary blue (#1F8FFF) used consistently
- [ ] Dark blue (#0D47A1) for accents
- [ ] Success green (#4CAF50) for approvals
- [ ] Danger red (#F44336) for rejections
- [ ] Warning yellow (#FFC107) for warnings
- [ ] Light blue (#E3F2FD) for backgrounds

### CSS Elements
- [ ] Gradient header renders correctly
- [ ] Metric cards have gradient backgrounds
- [ ] Left border (4px blue) on metric cards
- [ ] Rounded corners on cards (10px)
- [ ] Tables force white backgrounds
- [ ] Table text is dark and readable
- [ ] Buttons have hover effects
- [ ] Progress bars are blue
- [ ] Info/warning/success/danger boxes style correctly
- [ ] Email preview has monospace font
- [ ] Footer displays at bottom

### Responsive Design
- [ ] Layout adjusts to browser width
- [ ] Columns stack appropriately on narrow screens
- [ ] Charts remain readable
- [ ] Tables scroll horizontally if needed
- [ ] Sidebar collapsible on mobile

---

## ✅ Data Persistence

### CSV Operations
- [ ] Data loads on app start
- [ ] Only loads once per session
- [ ] Decisions append to decisions.csv
- [ ] Requests removed from invoice_requests.csv
- [ ] Audit entries append to audit_log.csv
- [ ] CSV files remain valid after writes
- [ ] No data corruption
- [ ] Proper date/datetime formatting
- [ ] Boolean values store as True/False
- [ ] Float precision maintained

### Session State
- [ ] Data stored in session state after load
- [ ] Updates happen in-memory first
- [ ] CSV saves occur on decisions
- [ ] Session state persists during navigation
- [ ] Counters increment correctly
- [ ] No data loss between pages
- [ ] Refresh button updates session state

---

## ✅ Error Handling

### Missing Files
- [ ] App handles missing CSV gracefully
- [ ] Creates empty dataframes with correct columns
- [ ] Sample data script regenerates files

### Invalid Data
- [ ] App handles empty CSVs
- [ ] Displays appropriate "No data" messages
- [ ] Doesn't crash on malformed data

### User Actions
- [ ] Can't submit without selecting request
- [ ] Can cancel decision before sending
- [ ] Appropriate feedback on all actions

---

## ✅ Performance

### Load Times
- [ ] Initial app load < 5 seconds
- [ ] Page switches < 1 second
- [ ] AI decision calculation < 2 seconds
- [ ] Chart rendering instant
- [ ] No noticeable lag

### Data Volume
- [ ] Handles 30 pending requests smoothly
- [ ] Handles 50 historical decisions
- [ ] Charts render with full dataset
- [ ] Filters respond instantly
- [ ] CSV exports complete quickly

---

## ✅ User Experience

### Intuitive Navigation
- [ ] Clear page labels
- [ ] Obvious next steps
- [ ] Back navigation works
- [ ] No dead ends

### Visual Feedback
- [ ] Success messages after actions
- [ ] Loading spinners where appropriate
- [ ] Hover effects on interactive elements
- [ ] Color coding aids comprehension

### Help & Guidance
- [ ] Instructions clear
- [ ] Context provided for decisions
- [ ] Tooltips helpful (if any)
- [ ] Error messages actionable

---

## ✅ Edge Cases

### Empty States
- [ ] Dashboard with no requests
- [ ] Review page with no pending requests
- [ ] Reports with no decisions
- [ ] Analytics with insufficient data
- [ ] Audit log empty

### Boundary Values
- [ ] Amount = 0
- [ ] Amount = very large number
- [ ] Extension days = 0
- [ ] Extension days = 30
- [ ] Scores at 0.0 and 1.0
- [ ] All priorities tested
- [ ] All cash flow impacts tested

### Workflow States
- [ ] Process last pending request
- [ ] Process first pending request
- [ ] Cancel decision multiple times
- [ ] Switch pages mid-decision
- [ ] Refresh during decision
- [ ] Multiple consecutive decisions

---

## ✅ Documentation

### README.md
- [ ] Complete and accurate
- [ ] Installation steps clear
- [ ] All features documented
- [ ] Examples helpful
- [ ] Troubleshooting section useful

### QUICKSTART.md
- [ ] Step-by-step instructions work
- [ ] First-time user friendly
- [ ] Testing scenarios valid
- [ ] Pro tips helpful

### Code Comments
- [ ] Functions documented
- [ ] Complex logic explained
- [ ] Configuration options noted
- [ ] Logo placeholder comments present

---

## 🎯 Final Verification

### Complete User Journey
- [ ] Install application ✓
- [ ] Launch successfully ✓
- [ ] View dashboard ✓
- [ ] Select and review a request ✓
- [ ] Read both explanation types ✓
- [ ] Make a decision ✓
- [ ] Preview and send email ✓
- [ ] Verify decision saved ✓
- [ ] Check reports updated ✓
- [ ] Export data ✓
- [ ] Refresh data ✓

### Quality Checks
- [ ] No console errors in browser
- [ ] No Python exceptions in terminal
- [ ] All linter checks pass
- [ ] CSV files remain valid
- [ ] Performance acceptable
- [ ] UI looks professional
- [ ] Keboola branding consistent

---

## 📋 Test Results

**Date Tested**: _________________

**Tested By**: _________________

**Version**: 1.0.0

**Overall Status**: ⬜ PASS   ⬜ FAIL   ⬜ NEEDS WORK

**Notes**:
```
[Add any issues, observations, or recommendations here]







```

---

## 🚀 Sign-Off

- [ ] All critical features working
- [ ] All tests passed
- [ ] Documentation complete
- [ ] Ready for production use

**Approved By**: _________________

**Date**: _________________

---

**Made with ❤️ by Keboola**

