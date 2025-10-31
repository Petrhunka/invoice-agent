# Quick Start Guide - Invoice Payment Manager

## 🚀 Installation (5 minutes)

### Step 1: Verify Prerequisites
```bash
# Check Python version (need 3.8+)
python3 --version

# Check pip
pip3 --version
```

### Step 2: Install Dependencies
```bash
# Navigate to project directory
cd invoice-agent

# Install required packages
pip3 install -r requirements.txt
```

Expected packages:
- streamlit (1.29.0)
- pandas (2.1.4)
- plotly (5.18.0)
- numpy (1.26.2)
- python-dateutil (2.8.2)

### Step 3: Verify Data Files
```bash
# Check if sample data exists
ls -la data/

# Should see:
# - invoice_requests.csv (30 records)
# - decisions.csv (50 records)
# - audit_log.csv (25 records)
```

If data files don't exist, generate them:
```bash
python3 generate_sample_data.py
```

### Step 4: Launch Application
```bash
# Option A: Use launch script
chmod +x run.sh
./run.sh

# Option B: Direct command
streamlit run main_simple.py
```

### Step 5: Access Application
Open your browser to: **http://localhost:8501**

**Note**: The application uses light theme by default for optimal readability. This is configured in `.streamlit/config.toml`.

---

## 📱 First-Time Usage

### What You'll See

**1. Dashboard (Home Page)**
- 4 metric cards showing current statistics
- 2 charts: Amount Distribution & Priority Breakdown
- Tables showing pending and recent requests

**2. Navigation**
- Use sidebar to switch between pages:
  - 🏠 Dashboard
  - 📋 Review Requests
  - 📊 Reports

**3. Quick Stats (Sidebar)**
- Pending count
- Processed count with approval rate
- Refresh button to reload CSV data

---

## 🎯 Try Your First Review

### Step-by-Step Walkthrough

**1. Go to Review Requests Page**
- Click "📋 Review Requests" in sidebar

**2. Select a Request**
- Use dropdown to select any pending request
- Example: "REQ-1001 - Strategic Services ($3,300.13)"

**3. Read Original Email (Left Column)**
- See vendor's payment extension request
- Note the reason and requested extension period

**4. Review AI Recommendation (Right Column)**
- See decision: ✅ APPROVED or ❌ REJECTED
- Check Confidence Score and Risk Score
- Read brief reasoning

**5. Explore AI Explanation**
- Click "View Detailed Explanation"
- Toggle between:
  - **💼 Business Explanation**: Color-coded factors with plain language
  - **🔬 Technical Explanation**: Formulas, calculations, metrics

**6. Make Your Decision**
- Click "✅ APPROVE" or "❌ REJECT" button

**7. Preview Email**
- Review the auto-generated response email
- Compare with original request

**8. Send & Complete**
- Click "📤 Send Email & Complete"
- See success message with balloons! 🎉

**9. Verify Changes**
- Go back to Dashboard
- See updated metrics
- Check Reports > Decision History

---

## 📊 Explore Reports

### Tab 1: All Pending Requests
- View all 30 pending requests
- Apply filters:
  - Priority (High/Medium/Low)
  - Amount range slider
  - Vendor multiselect
- Download filtered data as CSV

### Tab 2: Decision History
- View 50 historical decisions
- Filter by:
  - Decision type (Approved/Rejected)
  - Date range (days back slider)
  - Minimum confidence score
- Export to CSV

### Tab 3: Analytics
- **Line Chart**: Decisions over time
- **Box Plot**: Amount distribution by decision
- **Histogram**: Confidence score distribution
- **Summary Stats**: 4 key metrics

### Tab 4: Audit Log
- View all user activities
- Filter by action type and user
- Complete audit trail

---

## 🧪 Testing Scenarios

### Scenario 1: Approve a Low-Risk Request
1. Find request with:
   - Amount < $20,000
   - Extension ≤ 14 days
   - Vendor reliability > 85%
2. AI should recommend **APPROVED** with high confidence
3. Review business explanation (mostly 🟢 green indicators)
4. Approve and send email

### Scenario 2: Reject a High-Risk Request
1. Find request with:
   - Amount > $50,000
   - Extension > 21 days
   - Lower reliability scores
2. AI should recommend **REJECTED** with concerns
3. Review factors (more 🔴 red indicators)
4. Reject and send email

### Scenario 3: Explore Technical Explanation
1. Select any request
2. Open detailed explanation
3. Switch to "🔬 Technical Explanation"
4. Review:
   - Feature engineering table
   - Mathematical formulas (LaTeX)
   - Risk calculation steps
   - Decision tree logic
   - Performance metrics
   - Feature importance chart

### Scenario 4: Generate Reports
1. Process 2-3 requests (mix of approve/reject)
2. Go to Reports page
3. Check Tab 3: Analytics
4. See charts update with new data
5. Download CSV from Tab 2

---

## 🔧 Common Operations

### Refresh Data from CSV
- Click "🔄 Refresh from CSV" in sidebar
- Useful if someone else modified CSVs
- Or if you manually edited data files

### Export Data
- Go to Reports page
- Select any tab with data table
- Click "📥 Download CSV" button
- File saved with today's date in filename

### Add Your Own Requests
1. Edit `data/invoice_requests.csv`
2. Add new row following this format:
```csv
REQ-1031,Your Vendor,25000.00,2025-12-31,14,Your reason,Medium,0.85,0.82,Low,2025-10-24
```
3. Click refresh button in app
4. New request appears in dashboard

---

## ⚙️ Configuration

### Adjust Decision Thresholds
Edit `config.py`:
```python
DECISION_RULES = {
    "auto_approve_threshold": 0.8,    # Change to 0.85 for stricter
    "high_risk_amount": 50000,         # Lower to 40000 for more caution
    "min_confidence_score": 0.6,
}
```

### Change Risk Thresholds
```python
RISK_THRESHOLDS = {
    "amount": {
        "low": 20000,   # Adjust green/yellow boundary
        "high": 50000   # Adjust yellow/red boundary
    },
}
```

### Customize Colors
```python
KEBOOLA_COLORS = {
    "primary_blue": "#1F8FFF",    # Change main brand color
    "success_green": "#4CAF50",   # Change approval color
    # ... more colors
}
```

---

## 🐛 Troubleshooting

### "Module not found" Error
```bash
pip3 install -r requirements.txt --force-reinstall
```

### "Port 8501 already in use"
```bash
# Use different port
streamlit run main_simple.py --server.port 8502
```

### Data Not Loading
```bash
# Regenerate sample data
rm data/*.csv
python3 generate_sample_data.py
```

### App Crashes on Startup
```bash
# Check Python version (must be 3.8+)
python3 --version

# Clear Streamlit cache
rm -rf ~/.streamlit/
```

### Blank Tables Displaying
- This is a known Streamlit theme issue
- Tables have forced white backgrounds in CSS
- If still having issues, try:
  - Settings (top-right) → Theme → Light mode

---

## 📈 Usage Statistics

After processing several requests, check:

**Dashboard:**
- Session duration timer
- Processed count for current session
- Real-time approval rate

**Reports - Analytics Tab:**
- Total value processed
- Average processing time
- Approval rate trends
- Confidence score distribution

---

## 💡 Pro Tips

1. **Batch Processing**: Review multiple requests before making decisions
2. **Use Filters**: Find high-priority requests quickly in Reports
3. **Export Regularly**: Download decision history for records
4. **Review Patterns**: Check analytics to understand approval trends
5. **Audit Trail**: Use audit log to track all activities

---

## 🎓 Learning Resources

### Understanding AI Decisions
- Review the Technical Explanation for any request
- Study the decision tree logic
- Understand feature weights and their impact

### Business Context
- Business Explanation shows real-world factors
- Color coding helps quick risk assessment
- Factor impact table shows contribution breakdown

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Dashboard loads without errors
- [ ] Charts display with data
- [ ] Can select and review requests
- [ ] AI recommendation appears
- [ ] Both explanation types work
- [ ] Can approve a request
- [ ] Email preview generates
- [ ] Decision saves successfully
- [ ] Metrics update after decision
- [ ] Reports page shows data
- [ ] All 4 report tabs work
- [ ] CSV download works
- [ ] Audit log captures actions
- [ ] Refresh button reloads data

---

## 🎉 You're Ready!

The Invoice Payment Manager is now fully operational.

**Next Steps:**
1. Process a few sample requests to get comfortable
2. Customize thresholds to your organization's risk appetite
3. Add your own vendor data
4. Start processing real payment extension requests

**Need Help?**
- Check README.md for detailed documentation
- Review code comments in source files
- Contact support team

---

**Happy Processing! 🚀**

Made with ❤️ by Keboola

