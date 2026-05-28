"""CSS and styling utilities for the Streamlit dashboard."""
import streamlit as st


def load_custom_css() -> None:
    """Load modern premium CSS for dark theme styling."""
    st.markdown("""
<style>
    /* ===== MAIN BACKGROUND & LAYOUT ===== */
    .stApp {
        background: linear-gradient(135deg, #0F172A 0%, #1A1F3A 100%);
        color: #F8FAFC;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border-right: 1px solid rgba(51, 65, 85, 0.3);
    }
    
    /* ===== GLOBAL TEXT ===== */
    html, body, [class*="css"] { color: #F8FAFC; }
    
    /* ===== PREMIUM METRIC CARDS ===== */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1.5px solid rgba(100, 116, 139, 0.4);
        border-radius: 16px;
        padding: 24px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        border-color: rgba(100, 116, 139, 0.8);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    
    [data-testid="metric-container"] label {
        color: #64748B !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 12px !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 32px !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
        color: #10B981 !important;
        font-weight: 600 !important;
    }
    
    /* ===== HEADERS ===== */
    h1 {
        color: #F8FAFC !important;
        font-weight: 800 !important;
        font-size: 36px !important;
        letter-spacing: -0.02em;
        margin-bottom: 8px !important;
    }
    
    h2 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        font-size: 24px !important;
        margin-top: 24px !important;
        margin-bottom: 16px !important;
    }
    
    h3 {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 18px !important;
    }
    
    h4 {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
    }
    
    /* ===== DIVIDER ===== */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(51, 65, 85, 0.3), transparent);
        margin: 24px 0 !important;
    }
    
    /* ===== SELECT BOX & INPUTS ===== */
    .stSelectbox label,
    .stMultiSelect label {
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    /* ===== SIDEBAR RADIO BUTTONS ===== */
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    /* ===== SECTION LABELS ===== */
    .section-label {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        background: linear-gradient(90deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 12px;
        display: inline-block;
    }
    
    /* ===== PREMIUM INSIGHT CARDS ===== */
    .insight-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(20, 30, 50, 0.5) 100%);
        border: 1.5px solid rgba(100, 116, 139, 0.3);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        border-color: rgba(100, 116, 139, 0.6);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.25);
        transform: translateY(-2px);
    }
    
    .insight-card h4 {
        color: #60A5FA !important;
        font-size: 14px !important;
        margin-bottom: 8px;
        font-weight: 700;
    }
    
    .insight-card p {
        color: #CBD5E1;
        font-size: 13px;
        line-height: 1.7;
        margin: 0;
    }
    
    /* ===== DATAFRAME STYLING ===== */
    [data-testid="stDataFrame"] {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        border-radius: 12px;
        border: 1px solid rgba(51, 65, 85, 0.3);
    }
    
    /* ===== COLUMNS & CONTAINERS ===== */
    [data-testid="column"] {
        padding: 12px;
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #60A5FA 0%, #A78BFA 100%);
        color: white !important;
        border: 0;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 24px rgba(96, 165, 250, 0.3);
        transform: translateY(-2px);
    }
    
    /* ===== HIDE BRANDING ===== */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* ===== CUSTOM ANIMATION ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    [data-testid="metric-container"] {
        animation: fadeIn 0.5s ease forwards;
    }
</style>
""", unsafe_allow_html=True)
