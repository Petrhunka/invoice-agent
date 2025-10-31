"""
Custom Styling and UI Components for Invoice Payment Manager
Provides CSS injection and styled HTML components
"""

import streamlit as st
from config import KEBOOLA_COLORS


def load_custom_css():
    """Inject custom CSS styling into the Streamlit app"""
    
    css = f"""
    <style>
        /* Force Light Theme */
        .stApp {{
            background-color: #FFFFFF;
        }}
        
        /* Header Styling with Gradient */
        .main-header {{
            background: linear-gradient(135deg, {KEBOOLA_COLORS['primary_blue']} 0%, {KEBOOLA_COLORS['dark_blue']} 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white !important;
            text-align: center;
        }}
        
        .main-header h1 {{
            margin: 0 !important;
            padding: 0 !important;
            font-size: 2em !important;
            font-weight: 600 !important;
            color: white !important;
            display: block !important;
        }}
        
        .main-header p {{
            margin: 5px 0 0 0 !important;
            padding: 0 !important;
            font-size: 1em !important;
            opacity: 0.9 !important;
            color: white !important;
            display: block !important;
        }}
        
        /* Metric Card Styling */
        .metric-card {{
            background: linear-gradient(135deg, {KEBOOLA_COLORS['light_blue']} 0%, #FFFFFF 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid {KEBOOLA_COLORS['primary_blue']};
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 15px;
        }}
        
        .metric-card-title {{
            color: {KEBOOLA_COLORS['text_light']};
            font-size: 0.9em;
            margin-bottom: 8px;
            text-transform: uppercase;
            font-weight: 500;
        }}
        
        .metric-card-value {{
            color: {KEBOOLA_COLORS['primary_blue']};
            font-size: 2.2em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .metric-card-delta {{
            font-size: 0.85em;
            font-weight: 500;
        }}
        
        .metric-card-delta.positive {{
            color: {KEBOOLA_COLORS['success_green']};
        }}
        
        .metric-card-delta.negative {{
            color: {KEBOOLA_COLORS['danger_red']};
        }}
        
        .metric-card-delta.neutral {{
            color: {KEBOOLA_COLORS['text_light']};
        }}
        
        /* Button Styling */
        .stButton>button {{
            background-color: {KEBOOLA_COLORS['primary_blue']};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
            font-weight: 500;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            background-color: {KEBOOLA_COLORS['dark_blue']};
            box-shadow: 0 4px 8px rgba(31, 143, 255, 0.3);
        }}
        
        /* Info/Warning/Success/Danger Boxes */
        .info-box {{
            background-color: {KEBOOLA_COLORS['light_blue']};
            border-left: 4px solid {KEBOOLA_COLORS['primary_blue']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        
        .success-box {{
            background-color: #E8F5E9;
            border-left: 4px solid {KEBOOLA_COLORS['success_green']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        
        .warning-box {{
            background-color: #FFF3E0;
            border-left: 4px solid {KEBOOLA_COLORS['warning_yellow']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        
        .danger-box {{
            background-color: #FFEBEE;
            border-left: 4px solid {KEBOOLA_COLORS['danger_red']};
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }}
        
        /* Table Styling - Force Light Background */
        .dataframe {{
            background-color: #FFFFFF !important;
            color: {KEBOOLA_COLORS['text_dark']} !important;
        }}
        
        .dataframe td, .dataframe th {{
            background-color: #FFFFFF !important;
            color: {KEBOOLA_COLORS['text_dark']} !important;
            border: 1px solid #E0E0E0 !important;
            padding: 8px !important;
        }}
        
        .dataframe th {{
            background-color: {KEBOOLA_COLORS['light_blue']} !important;
            font-weight: 600 !important;
        }}
        
        .dataframe tr:nth-child(even) {{
            background-color: #FAFAFA !important;
        }}
        
        .dataframe tr:hover {{
            background-color: {KEBOOLA_COLORS['light_blue']} !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: {KEBOOLA_COLORS['neutral_gray']};
        }}
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {KEBOOLA_COLORS['text_dark']};
        }}
        
        /* Ensure all text is visible in light theme */
        .stMarkdown, .stText {{
            color: {KEBOOLA_COLORS['text_dark']};
        }}
        
        /* Radio buttons and selects */
        .stRadio label, .stSelectbox label, .stMultiSelect label {{
            color: {KEBOOLA_COLORS['text_dark']} !important;
        }}
        
        /* Tabs styling for light theme */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: #FFFFFF;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {KEBOOLA_COLORS['text_dark']};
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {KEBOOLA_COLORS['light_blue']};
            color: {KEBOOLA_COLORS['primary_blue']};
        }}
        
        /* Footer Styling */
        .footer {{
            text-align: center;
            padding: 20px;
            color: {KEBOOLA_COLORS['text_light']};
            font-size: 0.9em;
            margin-top: 50px;
            border-top: 1px solid #E0E0E0;
        }}
        
        /* Badge Styling */
        .badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
            margin: 2px;
        }}
        
        .badge-success {{
            background-color: {KEBOOLA_COLORS['success_green']};
            color: white;
        }}
        
        .badge-danger {{
            background-color: {KEBOOLA_COLORS['danger_red']};
            color: white;
        }}
        
        .badge-warning {{
            background-color: {KEBOOLA_COLORS['warning_yellow']};
            color: {KEBOOLA_COLORS['text_dark']};
        }}
        
        .badge-info {{
            background-color: {KEBOOLA_COLORS['primary_blue']};
            color: white;
        }}
        
        /* Factor Indicator Styling */
        .factor-card {{
            background-color: white;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }}
        
        .factor-header {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        
        .factor-indicator {{
            font-size: 1.5em;
            margin-right: 10px;
        }}
        
        .factor-name {{
            font-weight: 600;
            color: {KEBOOLA_COLORS['text_dark']};
        }}
        
        .factor-details {{
            font-size: 0.9em;
            color: {KEBOOLA_COLORS['text_light']};
            margin-top: 5px;
        }}
        
        /* Session Info Bar */
        .session-info {{
            background-color: {KEBOOLA_COLORS['light_blue']};
            padding: 10px 20px;
            border-radius: 5px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-around;
            text-align: center;
        }}
        
        .session-info-item {{
            flex: 1;
        }}
        
        .session-info-label {{
            font-size: 0.8em;
            color: {KEBOOLA_COLORS['text_light']};
            text-transform: uppercase;
        }}
        
        .session-info-value {{
            font-size: 1.2em;
            font-weight: 600;
            color: {KEBOOLA_COLORS['primary_blue']};
        }}
        
        /* Email Preview Styling */
        .email-preview {{
            background-color: #F9F9F9;
            border: 1px solid #E0E0E0;
            border-radius: 5px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            font-size: 0.9em;
            color: {KEBOOLA_COLORS['text_dark']};
            max-height: 600px;
            overflow-y: auto;
        }}
        
        /* Progress Bar Styling */
        .stProgress > div > div > div > div {{
            background-color: {KEBOOLA_COLORS['primary_blue']};
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


def render_metric_card(title, value, delta=None, icon="📊"):
    """
    Render a styled metric card
    
    Args:
        title: Card title
        value: Main value to display
        delta: Optional delta text
        icon: Optional icon/emoji
    
    Returns:
        HTML string for metric card
    """
    delta_html = ""
    if delta:
        delta_class = "neutral"
        if "↑" in str(delta) or "+" in str(delta):
            delta_class = "positive"
        elif "↓" in str(delta) or "-" in str(delta):
            delta_class = "negative"
        
        delta_html = f'<div class="metric-card-delta {delta_class}">{delta}</div>'
    
    html = f"""
    <div class="metric-card">
        <div class="metric-card-title">{icon} {title}</div>
        <div class="metric-card-value">{value}</div>
        {delta_html}
    </div>
    """
    
    return html


def render_colored_badge(text, badge_type="info"):
    """
    Render a colored badge
    
    Args:
        text: Badge text
        badge_type: Type of badge (success, danger, warning, info)
    
    Returns:
        HTML string for badge
    """
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def render_factor_indicator(factor_name, value, status, explanation, weight=None):
    """
    Render a factor indicator with color coding
    
    Args:
        factor_name: Name of the factor
        value: Value to display
        status: Status indicator ('green', 'yellow', 'red')
        explanation: Explanation text
        weight: Optional weight percentage
    
    Returns:
        HTML string for factor card
    """
    # Map status to emoji
    emoji_map = {
        'green': '🟢',
        'yellow': '🟡',
        'red': '🔴'
    }
    
    emoji = emoji_map.get(status, '⚪')
    
    weight_html = ""
    if weight is not None:
        weight_html = f'<span style="color: #757575; margin-left: 10px;">(Weight: {weight}%)</span>'
    
    html = f"""
    <div class="factor-card">
        <div class="factor-header">
            <span class="factor-indicator">{emoji}</span>
            <span class="factor-name">{factor_name}</span>
            {weight_html}
        </div>
        <div><strong>Value:</strong> {value}</div>
        <div class="factor-details">{explanation}</div>
    </div>
    """
    
    return html


def render_header_with_logo(logo_base64=None):
    """
    Render main header with optional logo
    
    Args:
        logo_base64: Base64 encoded logo image (optional)
    
    Returns:
        HTML string for header
    """
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="120" style="vertical-align: middle; margin-right: 15px;">'
    
    # Build header content
    title = "AI Invoice Auditor"
    subtitle = "Powered by Keboola"
    
    html = f'<div class="main-header">{logo_html}<h1>{title}</h1><p>{subtitle}</p></div>'
    
    return html


def render_session_info(duration, processed, approval_rate):
    """
    Render session info bar
    
    Args:
        duration: Session duration string
        processed: Number of processed requests
        approval_rate: Approval rate percentage
    
    Returns:
        HTML string for session info bar
    """
    html = f"""
    <div class="session-info">
        <div class="session-info-item">
            <div class="session-info-label">Session Duration</div>
            <div class="session-info-value">{duration}</div>
        </div>
        <div class="session-info-item">
            <div class="session-info-label">Processed This Session</div>
            <div class="session-info-value">{processed}</div>
        </div>
        <div class="session-info-item">
            <div class="session-info-label">Approval Rate</div>
            <div class="session-info-value">{approval_rate:.1f}%</div>
        </div>
    </div>
    """
    
    return html


def render_email_preview(email_text):
    """
    Render email preview with styling
    
    Args:
        email_text: Email content text
    
    Returns:
        HTML string for email preview
    """
    html = f"""
    <div class="email-preview">
{email_text}
    </div>
    """
    
    return html

