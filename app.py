"""
QC Pulse India — Quick Commerce Analytics Platform
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import warnings
import os
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─── PAGE CONFIG ────────────────────────────────────────────
st.set_page_config(
    page_title="QC Pulse India",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── GLOBAL CSS ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Base ── */
.stApp { background-color: #060B14; font-family: 'DM Sans', sans-serif; }
html, body, [class*="css"] { color: #E2E8F0; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1520 0%, #0A1018 100%);
    border-right: 1px solid #1E2D40;
}
[data-testid="stSidebar"] .stRadio label {
    color: #94A3B8 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    transition: color .15s;
}
[data-testid="stSidebar"] .stRadio label:hover { color: #F1F5F9 !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #0F1C2E 0%, #0D1823 100%);
    border: 1px solid #1E2D40;
    border-radius: 14px;
    padding: 18px 20px !important;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #DC2626, #7C3AED);
}
[data-testid="metric-container"] label {
    color: #64748B !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .1em !important;
    font-family: 'Space Mono', monospace !important;
}
[data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-size: 30px !important;
    font-weight: 700 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── Typography ── */
h1 {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    color: #F1F5F9 !important;
    font-size: 28px !important;
    letter-spacing: -.02em !important;
}
h2, h3 { color: #F1F5F9 !important; font-weight: 600 !important; }

/* ── Section labels ── */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0F1C2E 0%, #070D19 100%);
    border: 1px solid #1E2D40;
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
    box-shadow: 0 12px 48px rgba(0, 0, 0, 0.4);
}
.hero-left {
    flex: 1 1 450px;
}
.hero-stats {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    flex: 1 1 400px;
    justify-content: flex-end;
}
.hero-stat-card {
    background: #060B14;
    border: 1px solid #1E2D40;
    border-radius: 12px;
    padding: 16px 20px;
    min-width: 140px;
    text-align: center;
    flex: 1 1 140px;
    transition: transform 0.3s ease, border-color 0.3s ease;
}
.hero-stat-card:hover {
    transform: translateY(-3px);
    border-color: #7C3AED;
}
.hero-stat-value {
    font-size: 28px;
    font-weight: 700;
    color: #F1F5F9;
    font-family: 'Space Mono', monospace;
    background: linear-gradient(90deg, #DC2626, #7C3AED);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-stat-label {
    font-size: 10px;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-family: 'Space Mono', monospace;
    margin-top: 4px;
}

@keyframes statScale {
    0% { transform: scale(0.9); opacity: 0; filter: blur(3px); }
    100% { transform: scale(1); opacity: 1; filter: blur(0); }
}
.animate-stat {
    animation: statScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* ── Insight cards ── */
.insight-card {
    background: linear-gradient(135deg, #0F1C2E, #0D1823);
    border: 1px solid #1E2D40;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}
.insight-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #DC2626, transparent);
}
.insight-card h4 {
    color: #DC2626 !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: .1em !important;
    margin-bottom: 6px !important;
    font-family: 'Space Mono', monospace !important;
}
.insight-card p {
    color: #94A3B8;
    font-size: 13px;
    line-height: 1.65;
    margin: 0;
}
.insight-card .num {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    display: block;
    margin-bottom: 2px;
}

/* ── Stat badge ── */
.stat-badge {
    display: inline-block;
    background: rgba(220,38,38,.12);
    border: 1px solid rgba(220,38,38,.25);
    color: #FCA5A5;
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 99px;
    font-family: 'Space Mono', monospace;
    margin-bottom: 6px;
}

/* ── Divider ── */
hr { border-color: #1E2D40 !important; }

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px !important; overflow: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #060B14; }
::-webkit-scrollbar-thumb { background: #1E2D40; border-radius: 99px; }

/* ── Hide branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─── DATA LOADING ────────────────────────────────────────────
from utils.data_loader import load_data

try:
    bl, ze, bb, gr, rfm, rfm_sum, pm, cohort, sk, ar = load_data()
except Exception as e:
    st.error(f"❌ Data load failed: {e}")
    st.info("Make sure you've run all notebooks (01→07) first.")
    st.stop()


# ─── SIDEBAR ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 20px'>
        <div style='font-family:Space Mono,monospace;font-size:11px;
                    color:#DC2626;font-weight:700;letter-spacing:.1em;
                    text-transform:uppercase;margin-bottom:4px'>QC Pulse India</div>
        <div style='font-size:12px;color:#475569;line-height:1.5'>
            Quick Commerce<br>Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "nav",
        ["📊  Overview",
         "⚔️  Price Intelligence",
         "⭐  Review & Rating",
         "🛒  Market Basket",
         "👥  Customer Segments",
         "📈  Cohort Retention",
         "🌊  Customer Journey",
         "🎯  Business Simulator"],
        label_visibility="collapsed"
    )

    st.markdown("<hr style='border-color:#1E2D40;margin:16px 0'>", unsafe_allow_html=True)
    st.markdown("<p class='section-label'>Live Stats</p>", unsafe_allow_html=True)

    total_prod = len(bl) + len(ze) + len(bb)
    for icon, val, label in [
        ("🛒", f"{total_prod:,}", "products"),
        ("👥", f"{rfm['customer_id'].nunique():,}", "customers"),
        ("📦", f"{len(gr):,}", "transactions"),
        ("🏪", "3", "platforms analysed"),
        ("🔮", "3", "simulation models"),
        ("🤖", "ON", "auto-intelligence"),
    ]:
        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:10px;
                    padding:7px 0;border-bottom:1px solid #1E2D40'>
            <span style='font-size:14px'>{icon}</span>
            <div>
                <div style='font-size:14px;font-weight:700;color:#F1F5F9'>{val}</div>
                <div style='font-size:10px;color:#475569;text-transform:uppercase;
                            letter-spacing:.07em;font-family:Space Mono,monospace'>{label}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:10px;color:#334155;font-family:Space Mono,monospace;
                text-align:center;padding:8px 0'>
        Built by Yashaswini V<br>
        <span style='color:#DC2626'>●</span> May 2026
    </div>
    """, unsafe_allow_html=True)


# ─── CHART DEFAULTS ──────────────────────────────────────────
DARK_LAYOUT = dict(
    plot_bgcolor='#0D1823',
    paper_bgcolor='#0D1823',
    font=dict(color='#94A3B8', size=12, family='DM Sans'),
    margin=dict(l=10, r=10, t=36, b=10),
    xaxis=dict(color='#475569', gridcolor='#1E2D40', showgrid=True),
    yaxis=dict(color='#475569', gridcolor='#1E2D40', showgrid=True),
    hoverlabel=dict(bgcolor='#0F1C2E', bordercolor='#1E2D40',
                    font=dict(color='#F1F5F9', size=12))
)


# ─── VIEW ROUTING ─────────────────────────────────────────────
if "Overview" in page:
    from views.overview import render_overview
    render_overview(bl, ze, bb, gr, rfm, rfm_sum, cohort, pm, total_prod, DARK_LAYOUT)

elif "Price" in page:
    from views.price_intelligence import render_price_intelligence
    render_price_intelligence(bl, ze, bb, pm, DARK_LAYOUT)

elif "Review" in page or "Rating" in page:
    from views.review_rating import render_review_rating
    render_review_rating(bl, bb, DARK_LAYOUT)

elif "Basket" in page or "Market" in page:
    from views.market_basket import render_market_basket
    render_market_basket(ar, DARK_LAYOUT)

elif "Customer Seg" in page or "Segments" in page:
    from views.customer_segments import render_customer_segments
    render_customer_segments(rfm, rfm_sum, DARK_LAYOUT)

elif "Cohort" in page:
    from views.cohort_retention import render_cohort_retention
    render_cohort_retention(cohort, DARK_LAYOUT)

elif "Journey" in page:
    from views.customer_journey import render_customer_journey
    render_customer_journey(sk, DARK_LAYOUT)

elif "Simulator" in page:
    from views.business_simulator import render_business_simulator
    render_business_simulator(rfm, cohort, pm, DARK_LAYOUT)

# ─── PREMIUM FOOTER ───────────────────────────────────────────
st.markdown("<br><br><hr style='border-color:#1E2D40;'>", unsafe_allow_html=True)
st.markdown("""
<div style='display:flex; justify-content:space-between; align-items:center; 
            padding:12px 24px; background:linear-gradient(135deg, #0F1C2E 0%, #070D19 100%);
            border:1px solid #1E2D40; border-radius:12px; margin-top:20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3); flex-wrap: wrap; gap: 12px;'>
    <div style='font-family:Space Mono,monospace; font-size:11px; color:#64748B;'>
        © 2026 QC Pulse India · Decision Intelligence Engine
    </div>
    <div style='display:flex; gap:16px; font-family:Space Mono,monospace; font-size:11px;'>
        <span style='color:#DC2626;'>●</span> <span style='color:#94A3B8;'>Enterprise Grade</span>
        <span style='color:#1D9E75;'>●</span> <span style='color:#94A3B8;'>Auto-Intelligence Active</span>
        <span style='color:#6C63DB;'>●</span> <span style='color:#94A3B8;'>Secure Sandbox</span>
    </div>
</div>
<div style='font-size:10px; color:#334155; font-family:Space Mono,monospace; text-align:center; padding:15px 0 5px 0;'>
    Built for 15L+ D2C & Quick Commerce Analytics Roles · Yashaswini V
</div>
""", unsafe_allow_html=True)
