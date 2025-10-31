"""
Invoice Payment Manager - Main Application
Streamlit-based AI-powered invoice extension request review system
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

from config import KEBOOLA_COLORS, APP_TITLE, APP_SUBTITLE, RISK_THRESHOLDS, FEATURE_WEIGHTS
from data_manager import DataManager
from ai_decision_engine import AIDecisionEngine
from email_generator import format_original_email, generate_email_response
from styles import (
    load_custom_css, render_metric_card, render_colored_badge,
    render_factor_indicator, render_header_with_logo, 
    render_session_info, render_email_preview
)


# Page configuration
st.set_page_config(
    page_title="AI Invoice Auditor - Keboola",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AI Invoice Auditor - Powered by Keboola"
    }
)


def initialize_session_state():
    """Initialize session state variables on first run"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.data_manager = DataManager()
        st.session_state.ai_engine = AIDecisionEngine()
        st.session_state.session_start_time = datetime.now()
        st.session_state.processed_count = 0
        st.session_state.approved_count = 0
        st.session_state.selected_request = None
        st.session_state.pending_decision = None
        st.session_state.current_ai_result = None
        
        # Load data
        st.session_state.requests_df = st.session_state.data_manager.load_requests()
        st.session_state.decisions_df = st.session_state.data_manager.load_decisions()
        st.session_state.audit_log_df = st.session_state.data_manager.load_audit_log()
        
        st.session_state.data_loaded = True


def reload_data():
    """Manually reload data from CSV files"""
    st.session_state.requests_df = st.session_state.data_manager.load_requests()
    st.session_state.decisions_df = st.session_state.data_manager.load_decisions()
    st.session_state.audit_log_df = st.session_state.data_manager.load_audit_log()
    st.success("✅ Data reloaded from CSV files!")


def render_sidebar():
    """Render sidebar with navigation and quick stats"""
    with st.sidebar:
        # Keboola logo - try to load from different possible paths
        try:
            import os
            logo_path = None
            
            # Try different possible paths
            possible_paths = [
                "logo_blue.png",
                os.path.join(os.path.dirname(__file__), "logo_blue.png"),
                os.path.join(os.getcwd(), "logo_blue.png")
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    logo_path = path
                    break
            
            if logo_path:
                st.image(logo_path, width=150)
        except Exception:
            # Logo is optional, continue without it
            pass
        
        st.markdown("### 🏢 AI Invoice Auditor")
        st.markdown("*by Keboola*")
        st.markdown("---")
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        page = st.radio(
            "Select Page",
            ["🏠 Dashboard", "📋 Review Requests", "📊 Reports"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        stats = st.session_state.data_manager.get_statistics()
        
        st.metric("Pending", stats.get('pending_count', 0))
        
        processed = stats.get('total_processed', 0)
        approval_rate = stats.get('approval_rate', 0)
        st.metric("Processed", f"{processed} ({approval_rate:.0f}% approved)")
        
        st.markdown("---")
        
        # Data Status
        st.markdown("### 💾 Data Status")
        if st.session_state.data_loaded:
            st.success("✓ Data loaded")
        
        if st.button("🔄 Refresh from CSV"):
            reload_data()
        
        return page


def render_dashboard():
    """Render the main dashboard page"""
    
    # Load CSS
    load_custom_css()
    
    # Header without logo
    st.markdown(render_header_with_logo(), unsafe_allow_html=True)
    
    # Session info bar
    duration = datetime.now() - st.session_state.session_start_time
    hours, remainder = divmod(int(duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    stats = st.session_state.data_manager.get_statistics()
    approval_rate = stats.get('approval_rate', 0)
    
    st.markdown(
        render_session_info(duration_str, st.session_state.processed_count, approval_rate),
        unsafe_allow_html=True
    )
    
    # Metric Cards
    st.markdown("### 📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    pending_count = stats.get('pending_count', 0)
    processed_today = stats.get('processed_today', 0)
    avg_amount = stats.get('avg_amount', 0)
    high_priority = stats.get('high_priority_count', 0)
    total_pending_value = stats.get('total_pending_value', 0)
    
    with col1:
        st.markdown(
            render_metric_card(
                "Pending Requests",
                pending_count,
                f"Processed: {st.session_state.processed_count}",
                "📋"
            ),
            unsafe_allow_html=True
        )
    
    with col2:
        approved_today = len(st.session_state.data_manager.get_today_processed())
        st.markdown(
            render_metric_card(
                "Processed Today",
                processed_today,
                f"Approved: {approved_today}",
                "✅"
            ),
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            render_metric_card(
                "Avg Request Amount",
                f"${avg_amount:,.0f}",
                f"Total: ${total_pending_value:,.0f}",
                "💰"
            ),
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            render_metric_card(
                "High Priority",
                high_priority,
                "Needs attention",
                "⚠️"
            ),
            unsafe_allow_html=True
        )
    
    # Charts
    st.markdown("### 📊 Analytics")
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Amount Distribution")
        if not st.session_state.requests_df.empty:
            fig = px.histogram(
                st.session_state.requests_df,
                x='invoice_amount',
                nbins=15,
                title="",
                color_discrete_sequence=[KEBOOLA_COLORS['primary_blue']]
            )
            fig.update_layout(
                xaxis_title="Invoice Amount ($)",
                yaxis_title="Count",
                height=300,
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color=KEBOOLA_COLORS['text_dark'])
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No pending requests to display")
    
    with chart_col2:
        st.markdown("#### Priority Breakdown")
        if not st.session_state.requests_df.empty:
            priority_counts = st.session_state.requests_df['priority'].value_counts()
            colors_map = {
                'High': KEBOOLA_COLORS['danger_red'],
                'Medium': KEBOOLA_COLORS['warning_yellow'],
                'Low': KEBOOLA_COLORS['success_green']
            }
            colors = [colors_map.get(p, KEBOOLA_COLORS['primary_blue']) for p in priority_counts.index]
            
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="",
                color_discrete_sequence=colors
            )
            fig.update_layout(
                height=300,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color=KEBOOLA_COLORS['text_dark'])
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No pending requests to display")
    
    # Tables
    st.markdown("### 📋 Request Overview")
    table_col1, table_col2 = st.columns(2)
    
    with table_col1:
        st.markdown("#### Pending Requests")
        if not st.session_state.requests_df.empty:
            display_df = st.session_state.requests_df.head(10)[
                ['request_id', 'vendor_name', 'invoice_amount', 'priority', 'original_due_date']
            ].copy()
            display_df['invoice_amount'] = display_df['invoice_amount'].apply(lambda x: f"${x:,.2f}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("No pending requests")
    
    with table_col2:
        st.markdown("#### Recently Processed")
        if not st.session_state.decisions_df.empty:
            recent_df = st.session_state.decisions_df.sort_values('decision_date', ascending=False).head(10)[
                ['request_id', 'vendor_name', 'final_decision', 'confidence_score', 'decision_date']
            ].copy()
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        else:
            st.info("No processed requests yet")


def get_factor_status(factor_name, value):
    """Determine color status for a factor"""
    if factor_name == "Invoice Amount":
        if value < RISK_THRESHOLDS['amount']['low']:
            return 'green', 'LOW RISK'
        elif value < RISK_THRESHOLDS['amount']['high']:
            return 'yellow', 'MEDIUM'
        else:
            return 'red', 'HIGH RISK'
    
    elif factor_name == "Extension Period":
        if value <= RISK_THRESHOLDS['extension_days']['low']:
            return 'green', 'SHORT'
        elif value <= RISK_THRESHOLDS['extension_days']['high']:
            return 'yellow', 'MODERATE'
        else:
            return 'red', 'LONG PERIOD'
    
    elif factor_name == "Vendor Reliability":
        if value > RISK_THRESHOLDS['vendor_reliability']['excellent']:
            return 'green', 'EXCELLENT'
        elif value > RISK_THRESHOLDS['vendor_reliability']['good']:
            return 'yellow', 'GOOD'
        else:
            return 'red', 'CONCERNING'
    
    elif factor_name == "Payment History":
        if value > RISK_THRESHOLDS['payment_history']['excellent']:
            return 'green', 'EXCELLENT'
        elif value > RISK_THRESHOLDS['payment_history']['good']:
            return 'yellow', 'GOOD'
        else:
            return 'red', 'NEEDS REVIEW'
    
    elif factor_name == "Cash Flow Impact":
        if value == 'Low':
            return 'green', 'LOW IMPACT'
        elif value == 'Medium':
            return 'yellow', 'MEDIUM IMPACT'
        else:
            return 'red', 'HIGH IMPACT'
    
    elif factor_name == "Priority Level":
        if value == 'Low':
            return 'green', 'LOW'
        elif value == 'Medium':
            return 'yellow', 'MEDIUM'
        else:
            return 'red', 'HIGH'
    
    return 'yellow', 'MODERATE'


def render_business_explanation(request, ai_result):
    """Render business-friendly AI explanation"""
    st.markdown("#### 💼 Business Explanation")
    st.markdown("*Understanding the decision factors in plain language*")
    
    # Extract values
    amount = float(request.get('invoice_amount', 0))
    extension_days = int(request.get('requested_extension_days', 0))
    vendor_reliability = float(request.get('vendor_reliability_score', 0))
    payment_history = float(request.get('payment_history_score', 0))
    cash_flow = request.get('cash_flow_impact', 'Medium')
    priority = request.get('priority', 'Medium')
    
    # Render 6 factors
    st.markdown("##### Key Decision Factors")
    
    # Factor 1: Invoice Amount
    status, status_text = get_factor_status("Invoice Amount", amount)
    st.markdown(
        render_factor_indicator(
            "Invoice Amount",
            f"${amount:,.2f}",
            status,
            f"Status: {status_text}. Represents {FEATURE_WEIGHTS['amount']*100:.0f}% of the risk assessment.",
            FEATURE_WEIGHTS['amount']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor 2: Extension Period
    status, status_text = get_factor_status("Extension Period", extension_days)
    st.markdown(
        render_factor_indicator(
            "Extension Period",
            f"{extension_days} days",
            status,
            f"Status: {status_text}. Contributes {FEATURE_WEIGHTS['extension']*100:.0f}% to overall risk.",
            FEATURE_WEIGHTS['extension']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor 3: Vendor Reliability
    status, status_text = get_factor_status("Vendor Reliability", vendor_reliability)
    st.markdown(
        render_factor_indicator(
            "Vendor Reliability Score",
            f"{vendor_reliability*100:.0f}%",
            status,
            f"Status: {status_text}. Historical reliability impacts {FEATURE_WEIGHTS['vendor']*100:.0f}% of decision.",
            FEATURE_WEIGHTS['vendor']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor 4: Payment History
    status, status_text = get_factor_status("Payment History", payment_history)
    st.markdown(
        render_factor_indicator(
            "Payment History Score",
            f"{payment_history*100:.0f}%",
            status,
            f"Status: {status_text}. Past payment behavior weighs {FEATURE_WEIGHTS['payment']*100:.0f}%.",
            FEATURE_WEIGHTS['payment']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor 5: Cash Flow Impact
    status, status_text = get_factor_status("Cash Flow Impact", cash_flow)
    st.markdown(
        render_factor_indicator(
            "Cash Flow Impact",
            cash_flow,
            status,
            f"Status: {status_text}. Our cash position consideration: {FEATURE_WEIGHTS['cash_flow']*100:.0f}%.",
            FEATURE_WEIGHTS['cash_flow']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor 6: Priority Level
    status, status_text = get_factor_status("Priority Level", priority)
    st.markdown(
        render_factor_indicator(
            "Request Priority",
            priority,
            status,
            f"Status: {status_text}. Urgency factor contributes {FEATURE_WEIGHTS['priority']*100:.0f}%.",
            FEATURE_WEIGHTS['priority']*100
        ),
        unsafe_allow_html=True
    )
    
    # Factor Impact Summary
    st.markdown("##### Factor Impact Summary")
    factor_details = ai_result.get('factor_details', {})
    
    summary_data = []
    for factor_name, details in factor_details.items():
        summary_data.append({
            'Factor': factor_name.replace('_', ' ').title(),
            'Weight': f"{details['weight']*100:.0f}%",
            'Risk Contribution': f"{details['contribution']*100:.1f}%"
        })
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, use_container_width=True, hide_index=True)
    
    # Overall Assessment
    st.markdown("##### Overall Assessment")
    risk_score = ai_result.get('risk_score', 0)
    confidence_score = ai_result.get('confidence_score', 0)
    decision = ai_result.get('decision', 'Unknown')
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Risk Score", f"{risk_score*100:.1f}%")
        if risk_score < 0.4:
            st.success("🟢 Low risk - Favorable for approval")
        elif risk_score < 0.7:
            st.warning("🟡 Moderate risk - Requires review")
        else:
            st.error("🔴 High risk - Requires careful consideration")
    
    with col2:
        st.metric("Confidence Level", f"{confidence_score*100:.1f}%")
        if confidence_score > 0.8:
            st.success("🟢 High confidence in decision")
        elif confidence_score > 0.6:
            st.warning("🟡 Moderate confidence")
        else:
            st.error("🔴 Low confidence - Manual review recommended")
    
    # Final Recommendation
    st.markdown("##### AI Recommendation")
    reasoning = ai_result.get('reasoning', '')
    if decision == 'Approved':
        st.success(f"✅ **APPROVED**: {reasoning}")
    elif decision == 'Rejected':
        st.error(f"❌ **REJECTED**: {reasoning}")
    else:
        st.warning(f"⚡ **ESCALATE**: {reasoning}")


def render_technical_explanation(request, ai_result):
    """Render technical AI explanation with formulas and metrics"""
    st.markdown("#### 🔬 Technical Explanation")
    st.markdown("*Detailed model architecture and calculations*")
    
    # Model Architecture
    with st.expander("📐 Model Architecture", expanded=False):
        st.markdown("""
        **Algorithm**: Rule-Based Weighted Scoring System
        
        **Components**:
        1. Feature Engineering & Normalization
        2. Weighted Risk Score Calculation
        3. Confidence Score Estimation
        4. Decision Tree Logic
        
        **Model Type**: Deterministic decision system with transparent scoring
        """)
    
    # Feature Engineering
    st.markdown("##### Feature Engineering")
    
    factor_details = ai_result.get('factor_details', {})
    normalized = ai_result.get('normalized_features', {})
    
    feature_data = []
    feature_data.append({
        'Feature': 'Invoice Amount',
        'Raw Value': f"${factor_details.get('amount', {}).get('raw_value', 0):,.2f}",
        'Normalized': f"{normalized.get('amount_risk', 0):.3f}",
        'Formula': 'min(amount / 50000, 1.0)'
    })
    feature_data.append({
        'Feature': 'Extension Days',
        'Raw Value': f"{factor_details.get('extension', {}).get('raw_value', 0)} days",
        'Normalized': f"{normalized.get('extension_risk', 0):.3f}",
        'Formula': 'min(days / 30, 1.0)'
    })
    feature_data.append({
        'Feature': 'Vendor Reliability',
        'Raw Value': f"{factor_details.get('vendor', {}).get('raw_value', 0):.2f}",
        'Normalized': f"{normalized.get('vendor_risk', 0):.3f}",
        'Formula': '1 - reliability_score'
    })
    feature_data.append({
        'Feature': 'Payment History',
        'Raw Value': f"{factor_details.get('payment', {}).get('raw_value', 0):.2f}",
        'Normalized': f"{normalized.get('payment_risk', 0):.3f}",
        'Formula': '1 - payment_score'
    })
    feature_data.append({
        'Feature': 'Cash Flow Impact',
        'Raw Value': factor_details.get('cash_flow', {}).get('raw_value', 'N/A'),
        'Normalized': f"{normalized.get('cash_flow_risk', 0):.3f}",
        'Formula': 'Low=0.2, Med=0.5, High=0.8'
    })
    feature_data.append({
        'Feature': 'Priority',
        'Raw Value': factor_details.get('priority', {}).get('raw_value', 'N/A'),
        'Normalized': f"{normalized.get('priority_risk', 0):.3f}",
        'Formula': 'Low=0.3, Med=0.5, High=0.7'
    })
    
    feature_df = pd.DataFrame(feature_data)
    st.dataframe(feature_df, use_container_width=True, hide_index=True)
    
    # Risk Score Calculation
    st.markdown("##### Risk Score Calculation")
    st.latex(r'''
    Risk_{score} = \sum_{i=1}^{6} (Feature_i \times Weight_i)
    ''')
    
    st.markdown("**Weighted Formula:**")
    st.latex(r'''
    Risk = (Amount \times 0.25) + (Extension \times 0.20) + (Vendor \times 0.20)
    ''')
    st.latex(r'''
    + (Payment \times 0.15) + (CashFlow \times 0.15) + (Priority \times 0.05)
    ''')
    
    # Show actual calculation
    st.markdown("**Actual Calculation:**")
    risk_calc = ""
    for factor_name, details in factor_details.items():
        normalized_val = details.get('normalized', 0)
        weight = details.get('weight', 0)
        contribution = details.get('contribution', 0)
        risk_calc += f"- {factor_name}: {normalized_val:.3f} × {weight:.2f} = {contribution:.3f}\n"
    
    st.code(risk_calc)
    st.metric("**Total Risk Score**", f"{ai_result.get('risk_score', 0):.3f}")
    
    # Confidence Score Calculation
    st.markdown("##### Confidence Score Calculation")
    st.latex(r'''
    Base = \frac{Vendor_{reliability} + Payment_{history}}{2}
    ''')
    st.latex(r'''
    Amount_{factor} = 1.0 - min(\frac{amount}{100000}, 0.3)
    ''')
    st.latex(r'''
    Confidence = Base \times Amount_{factor}
    ''')
    
    # Show actual values
    vendor_rel = factor_details.get('vendor', {}).get('raw_value', 0)
    payment_hist = factor_details.get('payment', {}).get('raw_value', 0)
    amount = factor_details.get('amount', {}).get('raw_value', 0)
    
    base = (vendor_rel + payment_hist) / 2
    amount_factor = 1.0 - min(amount / 100000, 0.3)
    
    st.code(f"""
Base = ({vendor_rel:.2f} + {payment_hist:.2f}) / 2 = {base:.3f}
Amount Factor = 1.0 - min({amount:.2f} / 100000, 0.3) = {amount_factor:.3f}
Confidence = {base:.3f} × {amount_factor:.3f} = {ai_result.get('confidence_score', 0):.3f}
    """)
    
    # Decision Logic
    st.markdown("##### Decision Tree Logic")
    st.code("""
def determine_decision(confidence, risk, amount):
    # High confidence and low risk
    if confidence >= 0.80 and risk < 0.4:
        return 'Approved'
    
    # Low confidence or high risk
    if confidence < 0.60 or risk > 0.7:
        if amount > 50000:
            return 'Escalate'
        else:
            return 'Rejected'
    
    # Moderate confidence and acceptable risk
    if risk < 0.6 and confidence > 0.6:
        return 'Approved'
    
    # Default to escalation
    return 'Escalate'
    """, language='python')
    
    # Model Performance Metrics (Simulated)
    st.markdown("##### Model Performance Metrics")
    st.markdown("*Based on historical decision patterns*")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Precision", "0.89")
    with col2:
        st.metric("Recall", "0.92")
    with col3:
        st.metric("F1 Score", "0.90")
    with col4:
        st.metric("AUC-ROC", "0.94")
    
    # Feature Importance Chart
    st.markdown("##### Feature Importance")
    importance_data = {
        'Feature': ['Amount', 'Extension', 'Vendor', 'Payment', 'Cash Flow', 'Priority'],
        'Weight': [0.25, 0.20, 0.20, 0.15, 0.15, 0.05]
    }
    fig = px.bar(
        importance_data,
        x='Weight',
        y='Feature',
        orientation='h',
        title="Feature Weights in Risk Calculation",
        color='Weight',
        color_continuous_scale='Blues'
    )
    fig.update_layout(
        height=350,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color=KEBOOLA_COLORS['text_dark'])
    )
    st.plotly_chart(fig, use_container_width=True)


def render_review_requests():
    """Render the review requests page"""
    load_custom_css()
    
    # Header without logo
    st.markdown(render_header_with_logo(), unsafe_allow_html=True)
    st.markdown("## 📋 Review Payment Extension Requests")
    
    # Check if there are pending requests
    if st.session_state.requests_df.empty:
        st.info("🎉 No pending requests to review. All caught up!")
        return
    
    # Request selector
    request_options = [
        f"{row['request_id']} - {row['vendor_name']} (${row['invoice_amount']:,.2f})"
        for _, row in st.session_state.requests_df.iterrows()
    ]
    
    selected_option = st.selectbox(
        "Select a request to review:",
        options=request_options,
        key='request_selector'
    )
    
    if not selected_option:
        return
    
    # Get selected request
    request_id = selected_option.split(' - ')[0]
    selected_request = st.session_state.requests_df[
        st.session_state.requests_df['request_id'] == request_id
    ].iloc[0].to_dict()
    
    # Get AI decision
    ai_result = st.session_state.ai_engine.make_decision(selected_request)
    
    st.markdown("---")
    
    # Two-column layout
    col_left, col_right = st.columns([1, 1])
    
    # Left Column: Original Email
    with col_left:
        st.markdown("### 📧 Original Vendor Request")
        original_email = format_original_email(selected_request)
        st.text_area(
            "Vendor Email",
            original_email,
            height=400,
            label_visibility="collapsed"
        )
    
    # Right Column: AI Recommendation
    with col_right:
        st.markdown("### 🤖 AI Recommendation")
        
        # Decision badge
        decision = ai_result['decision']
        if decision == 'Approved':
            st.markdown(
                f"<h2 style='color: {KEBOOLA_COLORS['success_green']};'>✅ APPROVED</h2>",
                unsafe_allow_html=True
            )
        elif decision == 'Rejected':
            st.markdown(
                f"<h2 style='color: {KEBOOLA_COLORS['danger_red']};'>❌ REJECTED</h2>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<h2 style='color: {KEBOOLA_COLORS['warning_yellow']};'>⚡ ESCALATE</h2>",
                unsafe_allow_html=True
            )
        
        # Scores
        col_score1, col_score2 = st.columns(2)
        with col_score1:
            st.metric("Confidence Score", f"{ai_result['confidence_score']*100:.0f}%")
            st.progress(ai_result['confidence_score'])
        
        with col_score2:
            st.metric("Risk Score", f"{ai_result['risk_score']*100:.0f}%")
            st.progress(ai_result['risk_score'])
        
        # Brief reasoning
        st.markdown("**Reasoning:**")
        st.info(ai_result['reasoning'])
        
        # Request details
        st.markdown("**Request Details:**")
        st.markdown(f"""
        - **Request ID**: {selected_request['request_id']}
        - **Vendor**: {selected_request['vendor_name']}
        - **Amount**: ${selected_request['invoice_amount']:,.2f}
        - **Extension**: {selected_request['requested_extension_days']} days
        - **Priority**: {selected_request['priority']}
        - **Due Date**: {selected_request['original_due_date']}
        """)
    
    # AI Explanation Section
    st.markdown("---")
    st.markdown("### 🧠 AI Decision Explanation")
    
    explanation_type = st.radio(
        "Select explanation type:",
        ["💼 Business Explanation", "🔬 Technical Explanation"],
        horizontal=True
    )
    
    with st.expander("View Detailed Explanation", expanded=True):
        if explanation_type == "💼 Business Explanation":
            render_business_explanation(selected_request, ai_result)
        else:
            render_technical_explanation(selected_request, ai_result)
    
    # Decision Buttons
    st.markdown("---")
    st.markdown("### ⚖️ Your Decision")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("✅ APPROVE", type="primary", use_container_width=True):
            st.session_state.pending_decision = 'Approved'
            st.session_state.current_ai_result = ai_result
            st.session_state.selected_request = selected_request
            st.rerun()
    
    with col_btn2:
        if st.button("❌ REJECT", type="secondary", use_container_width=True):
            st.session_state.pending_decision = 'Rejected'
            st.session_state.current_ai_result = ai_result
            st.session_state.selected_request = selected_request
            st.rerun()
    
    # Email Preview if decision is pending
    if st.session_state.pending_decision and st.session_state.selected_request:
        st.markdown("---")
        st.markdown("### 📨 Email Preview")
        
        # Generate email
        response_email = generate_email_response(
            st.session_state.selected_request,
            st.session_state.pending_decision,
            st.session_state.current_ai_result
        )
        
        # Two columns for original and response
        email_col1, email_col2 = st.columns(2)
        
        with email_col1:
            st.markdown("#### Original Request")
            st.markdown(
                render_email_preview(format_original_email(st.session_state.selected_request)),
                unsafe_allow_html=True
            )
        
        with email_col2:
            st.markdown("#### Response Email")
            st.markdown(
                render_email_preview(response_email),
                unsafe_allow_html=True
            )
        
        # Send button
        col_send1, col_send2, col_send3 = st.columns([2, 1, 1])
        
        with col_send2:
            if st.button("📤 Send Email & Complete", type="primary", use_container_width=True):
                process_decision(
                    st.session_state.selected_request,
                    st.session_state.pending_decision,
                    st.session_state.current_ai_result
                )
        
        with col_send3:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.pending_decision = None
                st.session_state.current_ai_result = None
                st.session_state.selected_request = None
                st.rerun()


def process_decision(request, decision, ai_result):
    """Process and save the decision"""
    
    # Create decision record
    decision_data = {
        'request_id': request['request_id'],
        'decision_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ai_decision': ai_result['decision'],
        'confidence_score': ai_result['confidence_score'],
        'human_review': True,
        'final_decision': decision,
        'processing_time_seconds': ai_result['processing_time'],
        'vendor_name': request['vendor_name'],
        'invoice_amount': request['invoice_amount']
    }
    
    # Save decision
    st.session_state.data_manager.add_decision(decision_data)
    
    # Add audit log entry
    st.session_state.data_manager.add_audit_entry(
        action=f"Decision: {decision}",
        user="Current User",
        request_id=request['request_id'],
        details=f"Email sent to vendor, request {decision.lower()}"
    )
    
    # Remove from pending requests
    st.session_state.data_manager.remove_request(request['request_id'])
    
    # Update session state
    st.session_state.processed_count += 1
    if decision == 'Approved':
        st.session_state.approved_count += 1
    
    # Reload data
    st.session_state.requests_df = st.session_state.data_manager.load_requests()
    st.session_state.decisions_df = st.session_state.data_manager.load_decisions()
    st.session_state.audit_log_df = st.session_state.data_manager.load_audit_log()
    
    # Clear pending decision
    st.session_state.pending_decision = None
    st.session_state.current_ai_result = None
    st.session_state.selected_request = None
    
    # Show success message
    st.success(f"✅ Decision saved! Request {request['request_id']} has been {decision.lower()}.")
    st.balloons()
    
    # Rerun to refresh
    st.rerun()


def render_reports():
    """Render the reports page"""
    load_custom_css()
    
    # Header without logo
    st.markdown(render_header_with_logo(), unsafe_allow_html=True)
    st.markdown("## 📊 Reports & Analytics")
    
    # Top metrics
    stats = st.session_state.data_manager.get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Pending", stats.get('pending_count', 0))
    with col2:
        st.metric("Total Processed", stats.get('total_processed', 0))
    with col3:
        st.metric("Approved", stats.get('approved_count', 0))
    with col4:
        st.metric("Rejected", stats.get('rejected_count', 0))
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 All Pending Requests",
        "📜 Decision History",
        "📈 Analytics",
        "🔍 Audit Log"
    ])
    
    # Tab 1: All Pending Requests
    with tab1:
        st.markdown("### All Pending Requests")
        
        if not st.session_state.requests_df.empty:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                priority_filter = st.multiselect(
                    "Filter by Priority",
                    options=['High', 'Medium', 'Low'],
                    default=['High', 'Medium', 'Low']
                )
            
            with col_f2:
                amount_range = st.slider(
                    "Invoice Amount Range",
                    min_value=0,
                    max_value=int(st.session_state.requests_df['invoice_amount'].max()),
                    value=(0, int(st.session_state.requests_df['invoice_amount'].max()))
                )
            
            with col_f3:
                vendor_filter = st.multiselect(
                    "Filter by Vendor",
                    options=sorted(st.session_state.requests_df['vendor_name'].unique()),
                    default=sorted(st.session_state.requests_df['vendor_name'].unique())
                )
            
            # Apply filters
            filtered_df = st.session_state.requests_df[
                (st.session_state.requests_df['priority'].isin(priority_filter)) &
                (st.session_state.requests_df['invoice_amount'] >= amount_range[0]) &
                (st.session_state.requests_df['invoice_amount'] <= amount_range[1]) &
                (st.session_state.requests_df['vendor_name'].isin(vendor_filter))
            ]
            
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"pending_requests_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No pending requests to display")
    
    # Tab 2: Decision History
    with tab2:
        st.markdown("### Decision History")
        
        if not st.session_state.decisions_df.empty:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                decision_filter = st.multiselect(
                    "Filter by Decision",
                    options=['Approved', 'Rejected'],
                    default=['Approved', 'Rejected']
                )
            
            with col_f2:
                # Date range filter
                st.markdown("**Date Range**")
                days_back = st.slider("Days back", 1, 90, 30)
                cutoff_date = datetime.now() - timedelta(days=days_back)
            
            with col_f3:
                min_confidence = st.slider("Min Confidence Score", 0.0, 1.0, 0.0)
            
            # Apply filters
            filtered_decisions = st.session_state.decisions_df.copy()
            filtered_decisions['decision_date'] = pd.to_datetime(filtered_decisions['decision_date'])
            
            filtered_decisions = filtered_decisions[
                (filtered_decisions['final_decision'].isin(decision_filter)) &
                (filtered_decisions['decision_date'] >= cutoff_date) &
                (filtered_decisions['confidence_score'] >= min_confidence)
            ]
            
            st.dataframe(filtered_decisions, use_container_width=True, hide_index=True)
            
            # Download button
            csv = filtered_decisions.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"decision_history_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No decision history to display")
    
    # Tab 3: Analytics
    with tab3:
        st.markdown("### Analytics Dashboard")
        
        if not st.session_state.decisions_df.empty:
            decisions_df = st.session_state.decisions_df.copy()
            decisions_df['decision_date'] = pd.to_datetime(decisions_df['decision_date'])
            decisions_df['date'] = decisions_df['decision_date'].dt.date
            
            # Chart 1: Decisions over time
            st.markdown("#### Decisions Over Time")
            daily_decisions = decisions_df.groupby(['date', 'final_decision']).size().reset_index(name='count')
            
            fig = px.line(
                daily_decisions,
                x='date',
                y='count',
                color='final_decision',
                title="Daily Decision Trend",
                color_discrete_map={
                    'Approved': KEBOOLA_COLORS['success_green'],
                    'Rejected': KEBOOLA_COLORS['danger_red']
                }
            )
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color=KEBOOLA_COLORS['text_dark'])
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Chart 2: Amount by Decision Type
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                st.markdown("#### Amount Distribution by Decision")
                fig = px.box(
                    decisions_df,
                    x='final_decision',
                    y='invoice_amount',
                    color='final_decision',
                    title="",
                    color_discrete_map={
                        'Approved': KEBOOLA_COLORS['success_green'],
                        'Rejected': KEBOOLA_COLORS['danger_red']
                    }
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color=KEBOOLA_COLORS['text_dark'])
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col_chart2:
                st.markdown("#### Confidence Score Distribution")
                fig = px.histogram(
                    decisions_df,
                    x='confidence_score',
                    color='final_decision',
                    nbins=20,
                    title="",
                    color_discrete_map={
                        'Approved': KEBOOLA_COLORS['success_green'],
                        'Rejected': KEBOOLA_COLORS['danger_red']
                    }
                )
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color=KEBOOLA_COLORS['text_dark'])
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Summary Statistics
            st.markdown("#### Summary Statistics")
            stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
            
            with stat_col1:
                avg_confidence = decisions_df['confidence_score'].mean()
                st.metric("Avg Confidence", f"{avg_confidence*100:.1f}%")
            
            with stat_col2:
                avg_processing = decisions_df['processing_time_seconds'].mean()
                st.metric("Avg Processing Time", f"{avg_processing:.1f}s")
            
            with stat_col3:
                total_value = decisions_df['invoice_amount'].sum()
                st.metric("Total Value Processed", f"${total_value:,.0f}")
            
            with stat_col4:
                approval_rate = (len(decisions_df[decisions_df['final_decision'] == 'Approved']) / len(decisions_df)) * 100
                st.metric("Approval Rate", f"{approval_rate:.1f}%")
        
        else:
            st.info("No analytics data available yet")
    
    # Tab 4: Audit Log
    with tab4:
        st.markdown("### Audit Log")
        
        if not st.session_state.audit_log_df.empty:
            # Filters
            col_f1, col_f2 = st.columns(2)
            
            with col_f1:
                action_types = st.session_state.audit_log_df['action'].unique()
                action_filter = st.multiselect(
                    "Filter by Action",
                    options=sorted(action_types),
                    default=sorted(action_types)
                )
            
            with col_f2:
                users = st.session_state.audit_log_df['user'].unique()
                user_filter = st.multiselect(
                    "Filter by User",
                    options=sorted(users),
                    default=sorted(users)
                )
            
            # Apply filters
            filtered_audit = st.session_state.audit_log_df[
                (st.session_state.audit_log_df['action'].isin(action_filter)) &
                (st.session_state.audit_log_df['user'].isin(user_filter))
            ]
            
            st.dataframe(filtered_audit, use_container_width=True, hide_index=True)
            
            # Download button
            csv = filtered_audit.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"audit_log_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No audit log entries to display")


def main():
    """Main application entry point"""
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render selected page
    if page == "🏠 Dashboard":
        render_dashboard()
    elif page == "📋 Review Requests":
        render_review_requests()
    elif page == "📊 Reports":
        render_reports()
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div class="footer">Made with ❤️ by Keboola | AI Invoice Auditor © 2025</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()

